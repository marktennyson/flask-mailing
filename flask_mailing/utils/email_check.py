"""
Flask-Mailing v3.0.0 - Email Checker Module

Email validation utilities with optional Redis and HTTP support.
"""

from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import Any, ClassVar, cast

import dns.exception
import dns.resolver
from email_validator import validate_email as validator

from .errors import ApiError, DBProvaiderError

# Optional imports with better error handling
REDIS_AVAILABLE = False
HTTPX_AVAILABLE = False

try:
    import redis.asyncio as aioredis

    REDIS_AVAILABLE = True
except ImportError:
    aioredis = None  # type: ignore[assignment]

try:
    import httpx

    HTTPX_AVAILABLE = True
except ImportError:
    httpx = None  # type: ignore[assignment]


class AbstractEmailChecker(ABC):
    @abstractmethod
    def validate_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def is_dispasoble(self, email: str) -> bool:
        pass

    @abstractmethod
    async def check_mx_record(
        self, domain: str, full_result: bool = False
    ) -> bool | dict[str, Any]:
        pass

    @abstractmethod
    async def blacklist_add_email(self, email: str) -> None:
        pass

    @abstractmethod
    async def blacklist_add_domain(self, domain: str) -> None:
        pass

    @abstractmethod
    async def add_temp_domain(self, domain_lists: list[str]) -> None:
        pass

    @abstractmethod
    async def is_blocked_domain(self, domain: str) -> bool:
        pass

    @abstractmethod
    async def is_blocked_address(self, email: str) -> bool:
        pass

    @abstractmethod
    def catch_all_check(self) -> bool:
        pass


class DefaultChecker(AbstractEmailChecker):
    """
    Default class for checking email from collected public resource.
    The class makes it possible to use redis to save data.
    ```
    :param source(optional): source for collected email data.
    :param db_provider: switch to redis

    example:
        from flask_mailing.utils import DefaultChecker
        import asyncio

        a = DefaultChecker(db_provider="redis") # if you use redis
        loop = asyncio.get_event_loop()
        loop.run_until_complete(a.init_redis()) # Connect to redis and create default values
    ```
    """

    TEMP_EMAIL_DOMAINS: ClassVar[list[str]] = []
    BLOCKED_DOMAINS: ClassVar[set[str]] = set()
    BLOCKED_ADDRESSES: ClassVar[set[str]] = set()

    def __init__(
        self,
        source: str | None = None,
        db_provider: str | None = None,
        *,
        redis_host: str = "redis://localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        redis_pass: str | None = None,
        **options: Any,
    ) -> None:
        # Only require dependencies if using specific features
        if db_provider == "redis" and not REDIS_AVAILABLE:
            raise ImportError(
                "You must install aioredis from https://pypi.org/project/aioredis to use Redis functionality"
            )

        self.source = (
            source
            or "https://gist.githubusercontent.com/Turall/3f32cb57270aed30d0c7f5e0800b2a92/raw/dcd9b47506e9da26d5772ccebf6913343e53cec9/temporary-email-address-domains"
        )
        self.redis_enabled = db_provider == "redis"
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_pass = redis_pass
        self.options: dict[str, Any] = dict(options)
        self.redis_error_msg = "redis is not connected"
        self.redis_client: Any | None = None

    def _get_redis_client(self) -> Any:
        """Get the redis client, raising an error if not connected."""
        if self.redis_client is None:
            raise DBProvaiderError(self.redis_error_msg)
        return self.redis_client

    def catch_all_check(self) -> bool:
        frame = inspect.currentframe()
        func_name = frame.f_code.co_name if frame else "unknown"
        raise NotImplementedError(
            f"Func named {func_name} not implemented"
            f" for class {self.__class__.__name__}"
        )

    async def init_redis(self) -> bool:
        if not self.redis_enabled:
            raise DBProvaiderError(self.redis_error_msg)
        if self.redis_client is None and aioredis:
            redis_factory = cast("Any", aioredis)
            self.redis_client = await redis_factory.from_url(
                self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                password=self.redis_pass,
                **self.options,
            )
        if self.redis_client is None:
            raise DBProvaiderError(self.redis_error_msg)

        temp_counter = await self.redis_client.get("temp_counter")
        domain_counter = await self.redis_client.get("domain_counter")
        blocked_emails = await self.redis_client.get("email_counter")

        if not temp_counter:
            await self.redis_client.set("temp_counter", 0)
        if not domain_counter:
            await self.redis_client.set("domain_counter", 0)
        if not blocked_emails:
            await self.redis_client.set("email_counter", 0)
        temp_domains = await self.fetch_temp_email_domains()
        check_key = await self.redis_client.hgetall("temp_domains")
        if not check_key:
            kwargs = {
                domain: await self.redis_client.incr("temp_counter")
                for domain in temp_domains
            }
            await self.redis_client.hmset_dict("temp_domains", kwargs)

        return True

    def validate_email(self, email: str) -> bool:
        """Validate email address"""
        try:
            validator(email)
            return True
        except Exception:
            return False

    async def fetch_temp_email_domains(self) -> list[str]:
        """Fetch temporary email domains from the configured source URL."""
        if not httpx:
            raise ImportError("httpx is required for fetching temp email domains")

        async with httpx.AsyncClient() as client:
            response = await client.get(self.source)
            domains = response.text.splitlines()
            if self.redis_enabled:
                return domains

            self.TEMP_EMAIL_DOMAINS.extend(domains)
            return self.TEMP_EMAIL_DOMAINS

    async def blacklist_add_domain(self, domain: str) -> None:
        """Add domain to blacklist"""
        if self.redis_enabled:
            client = self._get_redis_client()
            result = await client.hget("blocked_domains", domain)
            if not result:
                incr = await client.incr("domain_counter")
                await client.hset("blocked_domains", domain, incr)
        else:
            self.BLOCKED_DOMAINS.add(domain)

    async def blacklist_rm_domain(self, domain: str) -> None:
        if self.redis_enabled:
            client = self._get_redis_client()
            res = await client.hdel("blocked_domains", domain)
            if res:
                await client.decr("domain_counter")
        else:
            self.BLOCKED_DOMAINS.remove(domain)

    async def blacklist_add_email(self, email: str) -> None:
        """Add email address to blacklist"""
        if self.validate_email(email):
            if self.redis_enabled:
                client = self._get_redis_client()
                blocked_domain = await client.hget("blocked_emails", email)
                if not blocked_domain:
                    inc = await client.incr("email_counter")
                    await client.hset("blocked_emails", email, inc)
            else:
                self.BLOCKED_ADDRESSES.add(email)

    async def blacklist_rm_email(self, email: str) -> None:
        if self.redis_enabled:
            client = self._get_redis_client()
            res = await client.hdel("blocked_emails", email)
            if res:
                await client.decr("email_counter")
        else:
            self.BLOCKED_ADDRESSES.remove(email)

    async def add_temp_domain(self, domain_lists: list[str]) -> None:
        """Manually add temporary email"""
        if self.redis_enabled:
            client = self._get_redis_client()
            for domain in domain_lists:
                temp_email = await client.hget("temp_domains", domain)
                if not temp_email:
                    incr = await client.incr("temp_counter")
                    await client.hset("temp_domains", domain, incr)
        else:
            self.TEMP_EMAIL_DOMAINS.extend(domain_lists)

    async def blacklist_rm_temp(self, domain: str) -> bool:
        if self.redis_enabled:
            client = self._get_redis_client()
            res = await client.hdel("temp_domains", domain)
            if res:
                await client.decr("temp_counter")
                return True
            return False

        if domain in self.TEMP_EMAIL_DOMAINS:
            self.TEMP_EMAIL_DOMAINS.remove(domain)
            return True
        return False

    async def is_dispasoble(self, email: str) -> bool:
        """Check email address is temporary or not"""
        if self.validate_email(email):
            _, domain = email.split("@")
            if self.redis_enabled:
                client = self._get_redis_client()
                result = await client.hget("temp_domains", domain)
                return bool(result)
            return domain in self.TEMP_EMAIL_DOMAINS
        return False

    async def is_blocked_domain(self, domain: str) -> bool:
        """Check blocked email domain"""
        if not self.redis_enabled:
            return domain in self.BLOCKED_DOMAINS

        client = self._get_redis_client()
        blocked_email = await client.hget("blocked_domains", domain)
        return bool(blocked_email)

    async def is_blocked_address(self, email: str) -> bool:
        """Check blocked email address"""
        if self.validate_email(email):
            if not self.redis_enabled:
                return email in self.BLOCKED_ADDRESSES

            client = self._get_redis_client()
            blocked_domain = await client.hget("blocked_emails", email)
            return bool(blocked_domain)
        return False

    async def check_mx_record(
        self, domain: str, full_result: bool = False
    ) -> bool | dict[str, Any]:
        """Check domain MX records"""

        try:
            mx_records = dns.resolver.resolve(domain, "MX")
            return (
                {"port": mx_records.port, "nameserver": mx_records.nameserver}
                if full_result
                else True
            )
        except (
            dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.NoNameservers,
            dns.exception.Timeout,
        ):
            return False

    async def blocked_email_count(self) -> int:
        """count all blocked emails in redis"""
        if self.redis_enabled:
            client = self._get_redis_client()
            value = await client.get("email_counter")
            return int(value or 0)
        return len(self.BLOCKED_ADDRESSES)

    async def blocked_domain_count(self) -> int:
        """count all blocked domains in redis"""
        if self.redis_enabled:
            client = self._get_redis_client()
            value = await client.get("domain_counter")
            return int(value or 0)
        return len(self.BLOCKED_DOMAINS)

    async def temp_email_count(self) -> int:
        """count all temporary emails in redis"""
        if self.redis_enabled:
            client = self._get_redis_client()
            value = await client.get("temp_counter")
            return int(value or 0)
        return len(self.TEMP_EMAIL_DOMAINS)

    async def close_connections(self) -> bool:
        """for correctly close connection from redis"""
        if self.redis_enabled:
            client = self._get_redis_client()
            await client.close()
            return True
        raise DBProvaiderError(self.redis_error_msg)


class WhoIsXmlApi:
    """
    WhoIsXmlApi class provide working with api  https://www.whoisxmlapi.com/ .
    This service gives free 1000 request to checking email address per month
    ```
    :param token: token you can get from this https://www.whoisxmlapi.com/ link
    :param email: email for checking

    example:
        from email_utils import WhoIsXmlApi

        who_is = WhoIsXmlApi(token="Your access token", email = "your@mailaddress.com")

        print(who_is.smtp_check_())  # check smtp server
        print(who_is.is_dispasoble()) # check email is disposable or not
        print(who_is.check_mx_record()) # check domain mx records
        print(who_is.free_check()) # check email domain is free or not
    ```
    """

    def __init__(self, token: str, email: str):
        self.token = token
        self.validate_email(email)
        self.email = email
        self.smtp_check = False
        self.dns_check = False
        self.free_check = False
        self.disposable = False
        self.catch_all = False
        self.mx_records: list[Any] = []
        self.host = "https://emailverification.whoisxmlapi.com/api/v1"

    async def fetch_info(self) -> bool:
        if not httpx:
            raise ImportError("httpx is required for WhoIsXmlApi integrations")
        async with httpx.AsyncClient() as client:
            params = {"apiKey": self.token, "emailAddress": self.email}
            response = await client.get(self.host, params=params)

            if response.status_code == 200:
                data = response.json()
                self.smtp_check = data["smtpCheck"]
                self.dns_check = data["dnsCheck"]
                self.free_check = data["freeCheck"]
                self.disposable = data["disposableCheck"]
                self.catch_all = data["catchAllCheck"]
                self.mx_records = data["mxRecords"]

                return True

        raise ApiError(
            f"Response status code is {response.status_code}, error msg {response.text}"
        )

    def validate_email(self, email: str) -> bool:
        """Validate email address"""
        try:
            validator(email)
            return True
        except Exception:
            return False

    def catch_all_check(self) -> bool:
        """
        Tells you whether or not this mail server has a “catch-all” address.
        This refers to a special type of address that can receive emails for any number of
        non-existent email addresses under a particular domain.
        Catch-all addresses are common in businesses where if you send an email to test@hi.com and
        another email to non-existent test2@hi.com, both of those emails will go into the same
        inbox.
        Possible values are 'true' or 'false'. May be 'null' for invalid or non-existing emails.
        """
        return self.catch_all

    def smtp_check_(self) -> bool:
        """
        Checks if the email address exists and
        can receive emails by using SMTP connection and
        email-sending emulation techniques.
        This value will be 'true' if the email address exists and
        can receive email over SMTP, and 'false' if the email address does not exist
        on the target SMTP server or temporarily couldn't receive messages.
        The value will be null if the SMTP request could not be completed,
        mailbox verification is not supported on the target mailbox provider, or not applicable.

        """
        return self.smtp_check

    def is_dispasoble(self) -> bool:
        """
        Tells you whether or not the email address is disposable (created via a service like
        Mailinator).
        This helps you check for abuse. This value will be 'false' if the email is not disposable,
        and 'true' otherwise.
        May be 'null' for invalid or non-existing emails.

        """
        return self.disposable

    def check_mx_record(self) -> list[Any]:
        """
        Mail servers list.
        May be absent for invalid or non-existing emails.
        """
        return self.mx_records

    def check_dns(self) -> bool:
        """
        Ensures that the domain in the email address, eg: gmail.com, is a valid domain.
        This value will be 'true' if the domain is good and 'false' otherwise.
        May be 'null' for invalid or non-existing emails.

        """
        return self.dns_check

    def check_free(self) -> bool:
        """
        Check to see if the email address is from a free email provider like Gmail or not.
        This value will be 'false' if the email address is not free, and 'true' otherwise.
        May be 'null' for invalid or non-existing emails.

        """
        return self.free_check

    def blacklist_add_email(self) -> None:
        frame = inspect.currentframe()
        func_name = frame.f_code.co_name if frame else "unknown"
        raise NotImplementedError(
            f"Func named {func_name} not implemented "
            f"for class {self.__class__.__name__}"
        )

    def blacklist_add_domain(self) -> None:
        frame = inspect.currentframe()
        func_name = frame.f_code.co_name if frame else "unknown"
        raise NotImplementedError(
            f"Func named {func_name} not implemented "
            f"for class {self.__class__.__name__}"
        )

    def add_temp_domain(self) -> None:
        frame = inspect.currentframe()
        func_name = frame.f_code.co_name if frame else "unknown"
        raise NotImplementedError(
            f"Func named {func_name} not implemented "
            f"for class {self.__class__.__name__}"
        )

    def is_blocked_domain(self) -> None:
        frame = inspect.currentframe()
        func_name = frame.f_code.co_name if frame else "unknown"
        raise NotImplementedError(
            f"Func named {func_name} not implemented "
            f"for class {self.__class__.__name__}"
        )

    def is_blocked_address(self) -> None:
        frame = inspect.currentframe()
        func_name = frame.f_code.co_name if frame else "unknown"
        raise NotImplementedError(
            f"Func named {func_name} not implemented "
            f"for class {self.__class__.__name__}"
        )

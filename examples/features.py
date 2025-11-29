from base import create_app
from flask import jsonify

from flask_mailing.utils import DefaultChecker, WhoIsXmlApi

app = create_app()


async def default_checker():
    checker = (
        DefaultChecker()
    )  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains()  # require to fetch temporary email domains
    return checker


@app.get("/email/dispasoble")
async def add_disp_domain():
    domains: list = ["gmail.com"]
    checker: DefaultChecker = await default_checker()

    res = await checker.add_temp_domain(domains)

    return jsonify(status_code=200, content={"result": res})


@app.get("/email/blocked/domains")
async def block_domain():
    domain: str = "gmail.com"
    checker: DefaultChecker = await default_checker()

    await checker.blacklist_add_domain(domain)

    return jsonify(status_code=200, content={"message": f"{domain} added to blacklist"})


@app.get("/email/blocked/check-domains")
async def get_blocked_domain():
    domain: str = "gmail.com"
    checker: DefaultChecker = await default_checker()
    res = await checker.is_blocked_domain(domain)

    return jsonify(status_code=200, content={"result": res})


@app.get("/email/blocked/address")
async def block_address():
    email: str = "hacker@gmail.com"
    checker: DefaultChecker = await default_checker()
    await checker.blacklist_add_email(email)

    return jsonify(status_code=200, content={"result": True})


@app.get("/email/blocked/address")
async def get_block_address():
    email: str = "hacker@gmail.com"
    checker: DefaultChecker = await default_checker()
    res = await checker.is_blocked_address(email)

    return jsonify(status_code=200, content={"result": res})


@app.get("/email/check-mx")
async def check_mx_record():
    checker = await default_checker()
    domain = "gmail.com"
    res = await checker.check_mx_record(domain, False)

    return jsonify(status_code=200, content={"result": res})


@app.get("/email/blocked/address")
async def del_blocked_address():
    checker = await default_checker()
    email = "hacker@gmail.com"
    res = await checker.blacklist_rm_email(email)

    return jsonify(status_code=200, content={"result": res})


@app.get("/email/blocked/domains")
async def del_blocked_domain():
    checker = await default_checker()
    domain = "gmail.com"
    res = await checker.blacklist_rm_domain(domain)

    return jsonify(status_code=200, content={"result": res})


@app.get("/email/dispasoblee")
async def del_disp_domain():
    checker = await default_checker()
    domains = ["gmail.com"]
    res = await checker.blacklist_rm_temp(domains)

    return jsonify(status_code=200, content={"result": res})


def show_whois_examples() -> None:
    who_is = WhoIsXmlApi(token="Your access token", email="your@mailaddress.com")

    print(who_is.smtp_check_())  # check smtp server
    print(who_is.is_dispasoble())  # check email is disposable or not
    print(who_is.check_mx_record())  # check domain mx records
    print(who_is.free_check)  # check email domain is free or not


if __name__ == "__main__":
    show_whois_examples()
    app.run(debug=True, port=8000)

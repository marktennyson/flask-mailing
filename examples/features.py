from base import create_app
from flask_email.utils import DefaultChecker
from flask import jsonify

app = create_app()

async def default_checker():
    checker = DefaultChecker()  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains() # require to fetch temporary email domains
    return checker

@app.get('/email/dispasoble')
async def add_disp_domain():
    domain: str = "gmail.com"
    domain_1:str = "yahoo.com"
    checker: DefaultChecker = await default_checker()

    await checker.blacklist_add_domain(domain)

    res = await checker.is_blocked_domain(domain_1)

    return jsonify(status_code=200, content={'result': res})

@app.get("/email/check-mx")
async def check_mx_record():
    checker = await default_checker()
    domain = "gmail.com"
    res = await checker.check_mx_record(domain, False)
    
    return jsonify(status_code=200, content={'result': res})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
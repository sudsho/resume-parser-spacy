from src.email_phone import find_emails, find_phones, find_urls


def test_basic_email():
    text = "contact me at john.doe@example.com any time"
    assert "john.doe@example.com" in find_emails(text)


def test_phone_indian():
    text = "phone: +91 98765 43210"
    phones = find_phones(text)
    assert any("98765" in p for p in phones)


def test_phone_us():
    text = "Call: +1-555-123-4567"
    phones = find_phones(text)
    assert any("555" in p and "4567" in p for p in phones)


def test_url():
    text = "see https://github.com/sudsho for more"
    urls = find_urls(text)
    assert "https://github.com/sudsho" in urls


def test_no_phone_in_year():
    # 2015 - 2019 is not a phone
    text = "I worked at Acme from 2015 to 2019"
    phones = find_phones(text)
    assert phones == []

# CAPTCHA Solving

**Category:** `web`
**Skill Level:** `advanced`
**Stability:** `experimental`

### Description

Solve CAPTCHAs during automated web interactions using third-party solving services (2Captcha, CapMonster), ML-based solvers, or human-in-the-loop escalation for high-security CAPTCHAs.

### Example

```python
import requests

# Submit CAPTCHA image to 2Captcha API
def solve_image_captcha(image_base64: str, api_key: str) -> str:
    resp = requests.post('https://2captcha.com/in.php', data={
        'key': api_key,
        'method': 'base64',
        'body': image_base64,
        'json': 1
    }).json()
    task_id = resp['request']

    import time
    time.sleep(10)  # wait for solve
    result = requests.get(
        f'https://2captcha.com/res.php?key={api_key}&action=get&id={task_id}&json=1'
    ).json()
    return result['request']  # solved text
```

> **Note:** Only use on sites you own or have permission to automate. CAPTCHA solving may violate ToS.

### Related Skills

- [Browser Navigation](browser-navigation.md)
- [Form Filling](form-filling.md)
- [Web Login](web-login.md)

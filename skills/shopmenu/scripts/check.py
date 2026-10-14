"""Check credential destination guards without fetching or printing a key."""
from query import BASE, NoRedirect, endpoint_url

assert endpoint_url('/v1/shops/清水亭/555458/menu') == BASE + '/v1/shops/%E6%B8%85%E6%B0%B4%E4%BA%AD/555458/menu'
for endpoint in ['https://example.com/v1/shops', '//example.com/v1/shops', '/v1/shops#fragment', '/other']:
    try:
        endpoint_url(endpoint)
    except ValueError:
        pass
    else:
        raise AssertionError('Unsafe endpoint accepted')
try:
    NoRedirect().redirect_request(None, None, 302, '', {}, 'http://example.com')
except ValueError:
    pass
else:
    raise AssertionError('Redirect accepted')
print('ShopMenu credential destination checks passed')

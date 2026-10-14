# API and local assets

Base URL: `http://129.211.210.83`. REST uses `X-API-Key`. All documented endpoints are GET-only.

| Endpoint | Result |
|---|---|
| `/v1/shops` | Shop records: id, mcId, name, brand, address, phone, logo, hasData, lastSync |
| `/v1/brands` | Brand names |
| `/v1/shops/{shop_id}/menu` | shop, categories, items |
| `/v1/shops/{shop_id}/categories` | Category list |
| `/v1/search?q=鱼头&brand=清水亭&limit=5` | Cross-shop item search |

Search accepts q (name/description/labels), brand (fuzzy), category (exact), min_price, max_price and limit (default 50, max 200). Prices are RMB yuan. Items include itemId, name, category, price, unit, description, image, labels, type (single/combo), isSale (1/0); search results add shopId, shopName and shopBrand. Image URLs are documented as public; verify availability when used.

Use the returned shop `id` as shop_id, including its slash; e.g. `/v1/shops/清水亭/555458/menu`. The helper URL-encodes Unicode paths and queries.

## Location and coverage

There is no separate city field in `/v1/shops`. Filter `address` for 沧州/黄骅; preserve the raw address and label any parsed city as derived. Empty addresses mean unknown location.

Live check on 2026-10-14 returned 23 brands and 32 shops, all hasData=true; source docs' 7 brands/16 shops count was stale. hasData is server metadata, not proof of completeness or freshness. lastSync values vary by shop.

Five addresses explicitly identified 河北省沧州市黄骅市:

| id | Name |
|---|---|
| 二小海鲜/2820520 | 二小海鲜·清真(黄骅新海西路店) |
| 天天鱼港/5273564 | 天天鱼港·海鲜·鲅鱼水饺·招牌烤鸭(黄骅店) |
| 早船炉烧鱼锅泡饼/129224319 | 早船炉烧鱼锅泡饼(黄骅店) |
| 星海一品/841615482 | 星海一品·海鲜酒楼 |
| 银海美食城/6143311 | 银海美食城 |

## Local trial dataset

Folder: `/Users/af/Public/APUCH/IPTrust/TableAI/education01/边江/侍天/menu_agent/`.

- `shopdatafetch_API_DOCS.md`: original connection documentation, retaining its plaintext API key at the user's request. A separate Keychain copy supports the query helper; keep this source document out of published skill repositories.
- `trial-details.jsonl`: 5 unique shop records, 63 stored reviews, validated on 2026-10-14; sha256 `04cab727e1b62f3b40e9ce1a2bf9ffa27f2b98e7e486cbca0ae7e905faf0e7c5`.

Trial shops: 锅圈露营火锅烤肉(南翠屏店), 必点海鲜·海肠捞饭(滨江道二店), 喜贵涮肉·五大道小院(天津首店), 小味道烤肉·焖锅, 馋小鲜川菜家常菜. Fields include shopid, shopuuid, list, full_name, sub_scores, rank, checkins_30d, open_status, hours, detail_tags, address, nearby_hint, no_star_reason, phones, listed_since, reviews, review_stats and optional good_rate_all_time. `list` includes cityid, area, rating, avg_price, review count, category, deals and tags.

This is a shop/review sample, not a full menu export. These shopid values are not the API's `brand/mcId` identifiers: establish a mapping before joining. Review times are relative and there is no capture timestamp; freshness is unknown. Stored reviews are samples, not total review counts.

## MCP alternative

Documented SSE URL: `http://129.211.210.83/mcp/sse`, with no extra authentication. Tools: list_shops, list_brands, get_menu(shop_id), get_categories(shop_id), search_menu(query, brand, category, min_price, max_price, max_results). MCP connectivity has not been tested; prefer the verified REST helper.

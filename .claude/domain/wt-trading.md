# WT 3.0 — Trading domain

Rules a tester needs to place, edit, close, and verify orders on the WebTrader member site (web, mobile-web, iOS, Android). Server = MT4 / MT5 / Centroid. Client = lirunex, transactCloud, centroid, hantec. Client and matrix definitions: `.claude/domain/wt-shared.md`. Screen locations: `.claude/domain/wt-member-site.md`.

Source paths below are relative to `ref-project/qa-automation-wt-3-0/`. Facts flagged `⚠ unverified` come with the reason. `<not in source>` = the value must come from the user.

**Precondition for every trade test: the symbol's market is open** (status `TRADING`, see §10). Forex symbols have no weekend session (src: `tests/conftest.py:219-228`).

## 1. Order placement

- Direction: `BUY` / `SELL` (src: `src/data/enums/trading.py:164`).
- Market order = 3 clicks: BUY (sets direction) → Place Order → Confirm (src: `.claude/lessons/manual-task-lessons.md:47`).
- Trade panel tabs: `Trade`, `One Click Trading`, `Specification`; `Chart` on mobile; `Market Depth` on Centroid only (src: `src/data/enums/trading.py:13-23`).

| Order type | Offered on | Note |
|---|---|---|
| market | all | |
| limit, stop | all | pending |
| stop limit | non-OMS clients only — transactCloud / hantec | pending; lirunex MT5 and Centroid do not show it (src: `src/data/enums/trading.py:175-193`) |

**One-Click Trading (OCT).**
- Preconditions: company flag `ONE_CLICK_TRADING` on in BO (`/backoffice/config/v1/oct`); the Settings option `One Click Trading` is absent when off (src: `src/api/webtrader/back_office/config.py:12-43`, `tests/web/conftest.py:76-90`, `src/data/enums/ui.py:365`).
- Where toggled: Settings → `One Click Trading` (web); Menu → Trade → `One-Click Trading` shortcut (mobile, opens the T&C sheet); trade panel tab `One Click Trading` (src: `src/data/enums/ui.py:92,412,439`, `enums/trading.py:15`).
- Activation modal text, in order (src: `src/data/ui_messages.py:83-94`): `Terms and Conditions` / `One-Click Trading enables trade execution with a single click, without any additional confirmations. Your order will be immediately submitted when you:` / `Click either the Sell or Buy buttons on the One-Click trading panel.` / `Click either the Place Sell Order or Place Buy Order buttons on the Trade trading panel.` / `Set or modify orders directly on the chart.` / `Close/delete orders in the positions' module or directly from the chart.` / `By clicking on Agree and continue below, I consent to the Terms and Conditions for activating One-Click Trading.` / button `Activate One-Click Trading`.
- Deactivation modal: `Confirm that you want to deactivate One-Click Trading?` / `Deactivate One-Click Trading`. Toasts: `One-Click Trading activated.` / `One-Click Trading deactivated.` Labels: `Activate One-Click Trading` / `Deactivate One-Click Trading` (src: `ui_messages.py:78-82,94`).
- What OCT skips: the confirmation modal on place, chart set/modify, and close/delete. The success toast still appears.

## 2. Order fields

**Volume label.** MT4 says `Size` / `Lot Size`; MT5 and Centroid say `Volume` (src: `enums/trading.py:62`, `objects/trade.py:411-412`). Error placeholders `%s` use `volume` / `size` / `quantity` (src: `ui_messages.py:210,220-221`; `quantity` = Centroid ⚠ unverified — inferred from Centroid's `Order Submitted` text, `objects/notification.py:93`).

**Units** = volume × contract size. Not shown on Centroid (src: `objects/trade.py:151-153`).

| Volume rule | Expectation | src |
|---|---|---|
| Valid | multiple of `Volume Step`, within `Min.`–`Max.` from Specification | `objects/trade.py:125-135` |
| Below min | `Minimum %s is %s` | `ui_messages.py:221`, `utils/random_utils.py:214-240` |
| Above max | `Maximum %s is %s` | `ui_messages.py:220` |
| Zero / not a step multiple | `Please enter a valid %s.` | `ui_messages.py:210` |
| Centroid test volumes | keep ≤ min × 2 | `objects/trade.py:131-132` |

**SL / TP.**
- Entered as `price` or `points` (src: `enums/trading.py:204-207`).
- Direction rule: BUY → SL below, TP above the closing (Sell) price. SELL → SL above, TP below the closing (Buy) price.
- Errors, `%s` filled per direction (src: `ui_messages.py:213-218`): `Stop Loss must be %s than %s Price.` (less|greater + Sell|Buy), `Take Profit must be %s than %s Price.` (greater|less + Sell|Buy), `Stop loss must be %s than take profit` (less for BUY, else greater), `Take profit must be %s than stop loss`, `Invalid Stop loss or Take profit`.
- Stop level floor: SL/TP distance ≥ symbol `Min. Stop Distance` (`stopsLevel`). Test data uses stop level + 20 points as the safe minimum (src: `utils/trading_utils.py:44`). Default stop level 12 when the symbol gives none (src: `objects/trade.py:22`).
- Centroid: no SL/TP on the place-order payload or in the place / pending-edit confirmation; open positions show `--` (src: `src/api/webtrader/member/trade.py:95-99`, `objects/trade.py:266-268,434-438`).

**Price (pending).** Stop BUY and Limit SELL sit above market; Stop SELL and Limit BUY sit below (src: `utils/trading_utils.py:143-146`). Reversed → `Invalid Price submitted.` / `Please enter a valid price.` / `Please enter a valid stop limit price.` (src: `ui_messages.py:211-213`).

**Expiry** (pending only; none on Centroid) (src: `enums/trading.py:210-236`, `objects/trade.py:297-345`):

| Value | Availability | Shown as |
|---|---|---|
| `Good Till Canceled` | default, MT4 + MT5 | `--` |
| `Good Till Day` | MT4 + MT5 | today's session close of the symbol, server tz (lirunex/centroid UTC+0, transactCloud/hantec UTC+3 — Centroid ⚠ unverified, `consts.py:48` "recheck for centroid") |
| `Specified Date` | MT5 only | date |
| `Specified Date and Time` | MT5 only | `YYYY-MM-DD HH:MM`, label `Expiry Date & Time` |

**Fill policy** — MT5 only, none on MT4 / Centroid. Market → `Fill or Kill` / `Immediate or Cancel`; pending → `Return`. The symbol's `tradeFillPolicy` can narrow the list (src: `enums/trading.py:259-290`).

**Time In Force** — Centroid only: `Fill or Kill`, `Immediate or Cancel`, `Good Till Canceled` (src: `enums/trading.py:308-311`).

**Direction-restricted symbols** (transactCloud, BO config, not in symbol API): `AUDUSD` BUY-only (confirmed release-SIT 2026-08-17), `BAKE.USD` SELL-only (src: `src/data/consts.py:50-54`). Expect the other button disabled, with OCT on and off.

## 3. Confirmation and edit modals

Confirmation (place order) (src: `objects/trade.py:383-471`):

| Field | MT4 / MT5 | Centroid |
|---|---|---|
| Symbol + description | mobile shows description | same |
| Order type | `BUY` / `SELL LIMIT` … | same |
| Volume / Size | yes | Volume |
| Units | yes | absent |
| Price (pending) | `Price` | `Price` |
| Stop Limit Price | stop-limit only | — |
| SL / TP | if set | absent on place and pending edit |
| Expiry (+ date) | pending | absent |
| Fill policy | MT5 | absent |
| Time In Force | — | yes |

Edit modal differences: non-Centroid mobile header `Order No. {id}`; Centroid market position header `Position ID {id}`, no order type, Time In Force fixed `Good Till Canceled` (src: `objects/trade.py:428-455`).

Edit position dialog fields (src: `objects/trade.py:473-500`): MT4/MT5 — symbol, order id, entry price, order type, volume, units, `One Point Equals`, fill policy (MT5). Centroid — symbol, order id, net volume, notional, Time In Force `Good Till Canceled`; avg entry price fluctuates, do not exact-match.

Close confirmation: symbol, order type, volume, order id. Centroid inverts the type (BUY position → `SELL`) and shows |net volume| (src: `objects/trade.py:522-539`). Delete-pending confirmation: fields above minus fill policy and expiry date; Centroid drops units (src: `objects/trade.py:502-520`).

## 4. Pre-trade details

Formulas (CFD) (src: `utils/trading_utils.py:487-540`). QER = quote currency exchange rate. Ref price = stop-limit price, else pending price, else live price.

| Row | Formula | Gate |
|---|---|---|
| `Trade Volume` (MT5) / `Trade Size` (MT4) | ref price × volume × contract size × QER (MT4: no QER) | Centroid label ⚠ unverified — "confirm with qa for centroid" `:498` |
| `Est. Margin Required` | contract size × volume × ref price × QER × margin% (× exchangeRate — ⚠ unverified on mobile, `:491-495`) | all |
| `Amount Per Tick` | `+/- ` point step × contract size × volume × QER | all |
| `Potential Loss \| Triggered by Stop Loss` | BUY (SL − ref) × mult; SELL (ref − SL) × mult | 0 on Centroid |
| `Potential Gain \| Triggered by Take Profit` | BUY (TP − ref) × mult; SELL (ref − TP) × mult | 0 on Centroid |
| `Risk:Reward` | `1 : ` gain ÷ loss | omitted on Centroid |

Open-position `Margin Used` = units × entry price / leverage (WT-14928) (src: `objects/trade.py:617-627`). Centroid: notional = |net volume| × contract size × market price; margin = notional × margin% (src: `objects/trade.py:184-186,257-258`).

**Tolerance.** These move with the feed; compare within a tolerance, never exact: close price, current price, profit/loss, SL/TP (points-derived), margin, margin used; market entry price; Centroid avg entry price, market price, notional, pending price (src: `objects/trade.py:278-294`).

## 5. Positions and orders (Assets)

Tabs (src: `enums/trading.py:326-435`):

| Tab | MT4 | MT5 | Centroid |
|---|---|---|---|
| `Open Positions`, `Pending Orders` | yes | yes | yes |
| `Positions History` | — | yes | — |
| `Orders & Deals History` | — | yes | — |
| `Order History` | yes | — | shown as `Orders History` (⚠ unverified — code comment says `All Orders`, `:330`) |
| `Transactions History` | — | — | yes |
| `Missed Trades`, `Copy Trade Profile` | copy trade (Pelican) only | | |

Deleted pending order lands in: MT4 `Order History`; MT5 `Orders & Deals History`; Centroid nowhere (src: `enums/trading.py:429-435`).

Web columns (excluding pinned Track / Edit / Close / Delete) (src: `objects/trade.py:751-840`):

| Tab | Server | Columns |
|---|---|---|
| Open Positions | MT5 | Open Date, Order No., Symbol, Type, Profit/Loss, ROI%, Volume, Units, Margin Used, Entry Price, Current Price, Take Profit, Stop Loss, Swap |
| Open Positions | MT4 | same with `Size`, plus `Commission` after Stop Loss |
| Open Positions | Centroid | Position ID, Symbol, Net Volume, Profit/Loss, ROI%, Avg Entry Price, Market Price, Notional, Take Profit, Stop Loss, Swap, Commission, Margin |
| Pending Orders | MT5 | Open Date, Order No., Symbol, Type, Volume, Units, Fill Policy, Expiry, Expiry Date, Price, Current Price, Take Profit, Stop Loss |
| Pending Orders | MT4 | Open Date, Order No., Symbol, Type, Size, Units, Expiry, Price, Current Price, Take Profit, Stop Loss |
| Pending Orders | Centroid | Order Date, Order ID, Symbol, Order Type, Price, Market Price, Volume, Fill Volume, Time-In-Force |
| Positions History | MT5 | Open Date, Symbol, Close Date, Order No., Type, Profit/Loss, Volume, Units, Entry Price, Close Price, Take Profit, Stop Loss, Swap, Commission, Remarks |
| Orders & Deals | MT5 | Open Date, Symbol, Close Date, Order No., Type, State, Volume, Units, Fill Policy, Entry Price, Take Profit, Stop Loss, Profit/Loss, Swap, Commission, Remarks |
| Order History | MT4 | Open Date, Close Date, Symbol, Order No., Status, Type, Profit/Loss, Size, Units, Entry Price, Close Price, Take Profit, Stop Loss, Swap, Commission, Remarks |
| Order History | Centroid | Date & Time, Order ID, Symbol, Order Type, Status, Avg Filled Price, Volume, Fill Volume, Time-In-Force, Market Range, Remarks |
| Transactions History | Centroid | ID, Symbol, Profit/Loss, Entry Price, Close Price, Volume, Open Date, Close Date, Type, Notional |

`Comment` column appears only when copy trade is enabled (after Swap on MT5, after Commission on MT4, appended on history tabs). `Symbol` hides when "hide other symbols" is on.

Mobile expanded-row labels (WT-12182) (src: `objects/trade.py:843-889`): Open Positions MT5 — Profit/Loss, ROI%, Status, Volume, Units, Margin Used, Entry Price, Current Price, Take Profit, Stop Loss, Swap, Open Date, Order No. (MT4: `Size`, plus Commission). Centroid — Profit/Loss, ROI%, Net Volume, Avg Entry Price, Market Price, Notional, Take Profit, Stop Loss, Margin, Swap, Commission, Position ID. Pending MT5 adds Fill Policy, Expiry, Expiry Date; `Stop Limit Price` row only for a stop-limit order. Pending Centroid — Volume, Fill Volume, Time-In-Force, Price, Market Price, Order Date, Order ID.

Status words and volume display (src: `objects/trade.py:541-670`):

| Where | Value |
|---|---|
| Mobile row status | `Open Position` / `Pending Order` |
| Positions History | `Closed` |
| Order History (MT4) | `Closed` position, `Canceled` pending |
| Orders & Deals | market `Filled`; closed position row shows the reverse type (BUY → `SELL`), deal `IN` / `OUT`; pending `Canceled`, or `Expired` with remark `Expired [<expiry>]` |
| Orders & Deals volume | filled `X / X`; pending `X / 0` |
| Positions History volume after partial close (MT5 web) | `closed / total` |
| Centroid Order History status | API status word, capitalised on mobile, UPPER on desktop web; market rows show the reverse type |

Volume buttons format: < 1 000 full; then `K` / `M` / `B` / `T`, floored to 2 dp, trailing zeros stripped (1 559 → `1.55K`) (src: `utils/format_utils.py:380-400`).

Assets sort/filter (mobile 3.0): `Order Type` filter chips for stop-limit ⚠ unverified — not rendered on release-SIT as of 2026-08-13, labels assumed (src: `enums/trading.py:541`).

## 6. Centroid netting

One position per symbol (src: `objects/trade.py:243-275`):
- Volumes are signed: BUY +, SELL −. Net volume = Σ signed volumes. Net volume 0 → the position disappears.
- Avg entry price = |Σ(volume × price)| / net volume.
- Market price column = bid when net > 0, ask when net < 0.
- SL / TP show `--`.
- Close volume max = |net volume|; the close order type is the inverse of the net side (src: `objects/trade.py:522-533`, `utils/trading_utils.py:585-590`).
- Opposite-direction placement reduces the net; same-direction adds to it and moves the avg entry price.
- Deleted pending orders leave no history row (§5).

## 7. Close, modify, delete

- Partial close: volume < position volume; a remaining position stays with reduced volume/units. Full close: volume = position volume (src: `objects/trade.py:169-240`).
- Close volume shortcuts: `min` (= Min. Volume), `25%`, `75%` (floored to Volume Step, never below Min.), `max` (src: `utils/trading_utils.py:543-603`).
- Toasts: `Position has been closed.` / `Position has been updated.` / `Failed to update position.` / `Order has been updated.` / `Order has been deleted.` (src: `ui_messages.py:98-100,130-131`). Centroid: `Position has been modified.` (src: `ui_messages.py:177`).

**Bulk close** (src: `enums/trading.py:438-449`, `ui_messages.py:103-116`):

| Option | Mobile label | Confirm | Web toast | Mobile title |
|---|---|---|---|---|
| `All Positions` | same | `Would you like to close all positions?` | `All positions have been closed.` | `Positions closed successfully.` |
| `Profitable Positions` | same | `Would you like to close all profitable positions?` | `All profitable positions have been closed.` | `Profitable Positions closed successfully.` |
| `Loss Positions` | `Losing Positions` | `Would you like to close all losing positions?` | `All losing positions have been closed.` | `Losing Positions closed successfully.` |

Mobile modal `Bulk Close Positions`, body `{n} positions have been closed.`, failure `Failed to close positions.` Centroid has no bulk close/delete API — the app closes one by one (src: `src/api/webtrader/member/trade.py:166,206`).

**Bulk delete** (src: `enums/trading.py:452-470`, `ui_messages.py:119-136`):

| Option | Mobile label | Confirm |
|---|---|---|
| `All Orders` | `Delete All Pending Orders` | `Would you like to delete all pending orders?` |
| `Limit Orders` | `Delete All Pending Limit Orders` | `Would you like to delete all limit orders?` |
| `Stop Orders` | `Delete All Pending Stop Orders` | `Would you like to delete all stop orders?` |
| `Stop Limit Orders` — non-OMS only | `Delete All Pending Stop Limit Orders` | `Would you like to delete all stop limit orders?` |

Mobile modal `Bulk Delete Pending Orders`. Cap note: `Note: A maximum of 30 %s will be deleted.` (`%s` = limit orders | stop orders | stop limit orders | pending orders). Success: `All %s have been deleted.` (web), `Pending orders deleted successfully.` / `Pending %s deleted successfully.` (mobile). Failure: `Failed to delete pending orders.` / `Please try again` / `Order action failed`.

Empty states: `You have no open positions.` / `You have no pending orders.` / `There are no trades.` / `There are no data.` / `No results found` (src: `ui_messages.py:139-140,149-150,235`).

## 8. Notifications and toasts

Toasts on place: `Position has been created.` (market), `Order has been created.` (pending) (src: `ui_messages.py:97,129`). Centroid-specific: `Order has been filled.` / `Order has been partially filled.` / `Order has been rejected.` / `Order has been submitted.` (src: `ui_messages.py:176-181`). Generic failure: `Trading general error. Please try again later.` (src: `ui_messages.py:10`).

Notification box (time `a few seconds ago`) (src: `objects/notification.py:9-115`):

| Event | Title | Content |
|---|---|---|
| Position opened (MT) | `Position Created` | `{symbol}  \|  Order No. {id} {BUY\|SELL} {volume} volume(s) at {entry}` (`size(s)` on MT4) |
| Position closed (MT) | `Position Closed \| {profit}` (`+` prefix when positive) | same shape, price = close price; suffix ` due to Stop Loss hit.` / ` due to Take Profit hit.` when SL/TP triggered (title then has no profit) |
| Order filled (Centroid) | `Order Filled \| FILLED` | `{symbol} \| Order ID:{id} {BUY\|SELL} {volume} volume(s) at {entry}` |
| Pending placed (Centroid) | `Order Pending \| NEW` | `{symbol} \| Order ID:{id} {BUY\|SELL} {LIMIT\|STOP} {volume} at {price}` |
| Rejected (Centroid) | `Order Rejected \| REJECTED` | ⚠ unverified — "recheck expected noti content" `:103` |
| Submitted (Centroid) | (none) | `Order Submitted \| {symbol} {BUY\|SELL} \| {type} Quantity: {volume}` |

Notification detail view: `Position Created` / `Position Closed` with symbol, type, order no., volume, units, entry price, SL, TP, commission `--`, swap `--`, remarks `--`; closed adds close price, profit/loss, and remarks (SL/TP hit) (src: `objects/notification.py:129-165`).

Symbol status from the market API: `TRADING` / `CLOSED` (src: `enums/trading.py:790-793`). Market closed → do not place; expected UI behaviour `<not in source>`.

## 9. Chart and Specification

Timeframes (src: `enums/trading.py:566-613`): MT5 full list — 1, 2, 3, 4, 5, 6, 10, 15, 20, 30 m; 1, 2, 3, 4, 6 H; 1D, 1W, 1M (minutes in a dropdown). MT4 and Centroid — 1m, 5m, 15m, 30m, 1H, 4H, 1D, 1W, 1M.
Indicators: main `BOLL, EMA, MA, SAR, WMA`; sub `ATR, CCI, MACD, RSI, SD, SO` (src: `enums/trading.py:667-713`). Types `Candlestick` / `Line`. Context menu: `Candlestick Color Setting`, `Remove all Drawing`, `Remove all Indicators`, `Remove all Indicators & Drawing`, `Show Ask Price on Y-axis`, `Clear All Track Details`, `Reset Chart` (src: `enums/trading.py:716-729`).

Specification tabs: `Symbol Overview` (Symbol, Description), `Trade Information`, `Trading Hours` (src: `enums/trading.py:48-85`).

| Trade Information row | MT5 | MT4 | Centroid |
|---|---|---|---|
| `Min. Volume`, `Max. Volume`, `Volume Step` | yes | `Min. Lot Size`, `Max. Lot Size`, `Lot Size Step` | yes |
| `One Point Equals`, `Contract Size`, `Margin Currency`, `Swap Type`, `Swap Long`, `Swap Short` | yes | yes | yes |
| `Min. Stop Distance`, `Margin Hedge`, `Initial Margin (%)`, `Maintenance Margin (%)`, `Swap Rollover (3 days)` | yes | yes | absent |
| `Margin Percentage`, `Swap Rollover` | — | — | yes |

`Swap Type` and `Swap Rollover`: desktop web renders text (e.g. code 0 → `in points`, rollover 3 → `Wednesday`); mobile shows the raw code (src: `enums/trading.py:25-45,101-117`).

Trading Hours `Time Display` row: company market timezone = SERVER (Root Admin) → sessions in server time, label `GMT +<offset>` (Centroid: `Server Time`); otherwise sessions in device local time, label `Local Time` (src: `enums/trading.py:134-159`).

## 10. Symbol tradability

Tradable = `enable` AND `online` AND `tradable` AND `tradableExeMode` AND not `holiday` AND `tradeMode == 2` AND has bid AND has ask (src: `src/data/objects/symbol.py:252-268`). Centroid symbol names are `FEED|SYMBOL` (src: `src/api/webtrader/back_office/configuration.py:45-48`).

## 11. Gates at a glance

| Rule | Applies to |
|---|---|
| Stop-limit order type, bulk-delete `Stop Limit Orders`, `Stop Limit Price` row | non-OMS clients: transactCloud, hantec |
| Fill policy, `Specified Date` / `Specified Date and Time`, Positions History, Orders & Deals, full timeframe list | MT5 |
| `Size` / `Lot Size` labels, `Commission` on Open Positions, Order History | MT4 |
| Time In Force, netting, Position ID, Notional / Margin, Market Depth tab, Transactions History, `Orders History`, `Margin Percentage`, no SL/TP on place, no expiry, no units, no bulk API, no pending-order history, P/L rows = 0, no Risk:Reward | Centroid |
| Units, expiry, SL/TP on place, `Order No.` | MT4 + MT5 |
| OCT toggle | company flag `ONE_CLICK_TRADING` on |
| `Comment` column | copy trade enabled |
| `Losing Positions`, `Delete All Pending …`, raw swap codes, `Open Position` / `Pending Order` status, `Chart` tab | mobile (iOS / Android / mobile-web) |
| `AUDUSD` buy-only, `BAKE.USD` sell-only | transactCloud |
| Market open (`TRADING`) | every trade test |

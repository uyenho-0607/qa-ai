# App Maestro Flows — OTC Member App (SIT)

App package: `com.bfgto.sit.app` · Device: `emulator-5556` (pixel6, Android 15)

## Structure

```
flows/app/
  launch-and-unlock.yaml          Launch app + passcode unlock
  nav-withdrawal-accounts.yaml    Navigate to Withdrawal accounts hub
  nav-crypto-addresses.yaml       Navigate to Crypto addresses
  add-bank-account.yaml           Full add bank account flow (parameterized)
  add-crypto-address.yaml         Full add crypto address flow (parameterized, unverified — see file)
  subflows/
    unlock.yaml                   Passcode unlock (conditional — only fires if screen visible)
    nav-linked-bank-accounts.yaml Navigate to Linked bank accounts from Home
    select-bank-country.yaml      Select a country from the country sheet
    select-currency.yaml          Select a currency from the currency sheet
    select-network.yaml           Select a network from the network sheet (single tap, no Done)
    verify-email-otp.yaml         Enter 6-digit email OTP
    nav-tap-withdraw.yaml         Tap Home's unlabeled Withdraw icon button
    nav-tap-deposit.yaml          Tap Home's unlabeled Deposit icon button
```

## Running

```bash
# Run with default env values
maestro test flows/app/add-bank-account.yaml

# Override env values
maestro test flows/app/add-bank-account.yaml \
  -e LABEL="My Test Account" \
  -e COUNTRY_NAME="Hong Kong" \
  -e BANK_NAME="HSBC" \
  -e CURRENCY_NAME="Hong Kong Dollar" \
  -e ACCOUNT_NAME="TEST USER" \
  -e ACCOUNT_NUMBER="1234567890" \
  -e BIC_SWIFT="HSBCHKHHHKH" \
  -e ADDRESS="1 Test St" \
  -e CITY="Hong Kong" \
  -e OTP="123456"
```

## Key Lessons

| Issue | Fix |
|---|---|
| `inputText` focuses a field that was searched — next tap goes to wrong element | Always `hideKeyboard` after every `inputText` before the next `tapOn` |
| `tapOn: text: "SGD"` matches the search field (which contains "SGD") instead of the result row | Use `scrollUntilVisible` + `tapOn: text: "Singapore Dollar"` (full currency name) instead of the code |
| Currency sheet — tapping by code after search requires 2 taps (first dismisses IME) | Use scroll-based selection without search to avoid the double-tap issue |
| Country sheet — `pressKey: Enter` after search does NOT select the country | `hideKeyboard` then `tapOn: text: ${COUNTRY_NAME}` to select |
| Add bank account header `+` button has no testID/label when list is non-empty | Use `tapOn: point: "94%,8%"` (top-right area) — unaddressable until app team adds testID |
| `otp-cell-0` testID not found after `launchApp` restarts the app | For OTP screens with no other input: `tapOn: text: "Verify your email"` focuses the OTP field — same pattern as passcode unlock. `inputText` the 6 digits, screen self-submits. |
| `scrollDown` is not a valid Maestro command | Use `scroll` or `swipe: direction: UP` |
| `tapOn: Done` does NOT close the keyboard (it only fires the IME action) | `pressKey: Back`. While the keyboard is up, Gboard's suggestion strip holds the literal search term and steals every text selector |
| A tap right after `inputText` silently misses — the filtered list has not settled. `waitForAnimationToEnd` is not a barrier | Gate on `extendedWaitUntil` (keyboard gone, then result visible), and wrap the tap in `retry` with `waitToSettleTimeoutMs` |
| A modal sheet does NOT hide the form behind it from the a11y tree, so an already-selected value competes with the sheet's own rows | Do not rely on a bare `tapOn: text:` inside a sheet; disambiguate or address by position |
| `below: text: "<placeholder>"` stops anchoring once the field has text (hint is a separate attribute) | Anchor on something outside the field, or address by position |
| Hardcoded pixel points (`613,662`) are bound to 1080x2400 and fail silently when they miss | Use percentages (`57%,28%`) and always follow with an assertion that proves the tap worked |
| `tapOn: text: "Bank country"` is ambiguous — the section label and the field both carry it | Tap the field by its current value, or by its placeholder `Select country` |
| Home's Deposit/Convert/Withdraw are unlabeled icon buttons; the visible word is a separate non-clickable TextView | `tapOn: text: "Withdraw"` no-ops silently — tap by point (`subflows/nav-tap-withdraw.yaml` / `nav-tap-deposit.yaml`) |
| Network sheet (Add crypto address) | Single tap selects and closes — no search, no Done button, unlike country/currency |

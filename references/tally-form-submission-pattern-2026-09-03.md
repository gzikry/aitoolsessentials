# Tally form submission pattern (2026-09-03)

Directory and vendor forms sometimes embed Tally forms (`tally.so/r/...` or `tally.so/embed/...`). Tally uses React's synthetic event system, so standard `fill_input` sets the DOM value but React doesn't detect the change — the form submits empty.

## Workaround: native value setter + event dispatch

```javascript
const fields = [
  {placeholder: 'Your Name', value: 'AIToolsEssentials'},
  {placeholder: 'Contact Email Address', value: 'contact@aitoolsessentials.com'},
  {placeholder: 'Tool Name', value: 'AIToolsEssentials'},
  {placeholder: 'Tool URL', value: 'https://aitoolsessentials.com'},
  {placeholder: 'Screenshot URL', value: 'https://aitoolsessentials.com/assets/aitools-bot-logo-256.png'}
];

for (const field of fields) {
  const input = document.querySelector(`input[placeholder="${field.placeholder}"]`);
  if (input) {
    input.focus();
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    nativeInputValueSetter.call(input, field.value);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    input.dispatchEvent(new Event('blur', { bubbles: true }));
  }
}
```

## Selecting radio buttons

After filling text inputs, click radio buttons normally via `.click()` — they don't use React's synthetic event system for state.

## Submitting

Find the submit button via `document.querySelector('button[type="submit"]')` and click it.

## Verification

After submit, check the page for success messages like "Thanks for your contribution" or "Submitted successfully".

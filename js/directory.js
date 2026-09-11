const input = document.querySelector('#toolSearch');
const cards = [...document.querySelectorAll('.directory-card')];
const count = document.querySelector('#toolCount');
if (input) input.addEventListener('input', () => {
  const q = input.value.trim().toLowerCase();
  let shown = 0;
  for (const card of cards) {
    const text = card.innerText.toLowerCase();
    const hidden = Boolean(q) && !text.includes(q);
    card.hidden = hidden;
    if (!hidden) shown += 1;
  }
  if (count) count.textContent = shown + ' of ' + cards.length + ' tools shown';
});

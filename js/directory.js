const input = document.querySelector('#toolSearch');
const cards = [...document.querySelectorAll('.directory-card')];
if (input) input.addEventListener('input', () => {
  const q = input.value.trim().toLowerCase();
  for (const card of cards) {
    const text = card.innerText.toLowerCase();
    card.hidden = q && !text.includes(q);
  }
});

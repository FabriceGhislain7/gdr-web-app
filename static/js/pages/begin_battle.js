document.addEventListener('DOMContentLoaded', function () {
  const checkboxes = document.querySelectorAll('input[name="selected_chars"]');
  const submitBtn = document.getElementById('submit-battle');

  function toggleButton() {
    const selected = Array.from(checkboxes).some(cb => cb.checked);
    submitBtn.disabled = !selected;
  }

  toggleButton();
  checkboxes.forEach(cb => cb.addEventListener('change', toggleButton));
});


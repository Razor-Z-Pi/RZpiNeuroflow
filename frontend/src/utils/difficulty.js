export function getDifficulty(type) {
  const raw = localStorage.getItem(`nf_diff_${type}`);
  return raw ? parseFloat(raw) : 1.0;
}

export function setDifficulty(type, value) {
  const clamped = Math.max(0.6, Math.min(1.5, value));
  localStorage.setItem(`nf_diff_${type}`, clamped.toFixed(2));
}

export function adjustAfter(type, accuracy) {
  const current = getDifficulty(type);
  if (accuracy < 60) {
    setDifficulty(type, current - 0.1);
  } else if (accuracy > 90) {
    setDifficulty(type, current + 0.1);
  }
}
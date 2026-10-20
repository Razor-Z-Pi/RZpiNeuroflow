const KEY = "nf_seen_hints";

function load() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || "[]");
  } catch {
    return [];
  }
}

export function hasSeen(key) {
  return load().includes(key);
}

export function markSeen(key) {
  const seen = load();
  if (!seen.includes(key)) {
    seen.push(key);
    localStorage.setItem(KEY, JSON.stringify(seen));
  }
}

export function resetAll() {
  localStorage.removeItem(KEY);
}
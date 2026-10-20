const QUEUE_KEY = "nf_offline_queue";

export function getQueue() {
  try {
    return JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
  } catch {
    return [];
  }
}

export function enqueue(payload) {
  const queue = getQueue();
  queue.push({ ...payload, _queuedAt: Date.now() });
  localStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
}

export function clearQueue() {
  localStorage.removeItem(QUEUE_KEY);
}

export function queueSize() {
  return getQueue().length;
}
export function buildHeatmap(history, weeks = 26) {
  const countsByDate = {};
  for (const item of history) {
    const d = item.date.slice(0, 10);
    countsByDate[d] = (countsByDate[d] || 0) + 1;
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);
  // Встаём на начало недели (понедельник)
  const start = new Date(today);
  const dayOfWeek = (start.getDay() + 6) % 7; // 0 = пн
  start.setDate(start.getDate() - dayOfWeek - (weeks - 1) * 7);

  const cells = [];
  const cursor = new Date(start);
  while (cursor <= today) {
    const key = cursor.toISOString().slice(0, 10);
    cells.push({
      date: key,
      count: countsByDate[key] || 0,
      isFuture: false,
    });
    cursor.setDate(cursor.getDate() + 1);
  }
  return cells;
}

export function levelFor(count) {
  if (count === 0) return 0;
  if (count === 1) return 1;
  if (count === 2) return 2;
  if (count === 3) return 3;
  return 4;
}
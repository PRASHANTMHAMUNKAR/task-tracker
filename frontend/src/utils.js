export function cleanTitle(value) {
  return String(value ?? "").trim();
}

export function isValidTitle(value) {
  const t = cleanTitle(value);
  return t.length > 0 && t.length <= 100;
}

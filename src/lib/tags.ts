function slugifyTag(tag: string): string {
  return tag
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function tagClass(tag: string): string {
  return `badge-${slugifyTag(tag)}`;
}

export function thumbClass(tag: string): string {
  return `thumb-${slugifyTag(tag)}`;
}

export function formatDate(date: Date): string {
  return date.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' });
}

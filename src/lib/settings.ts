import { getCollection } from 'astro:content';

export async function getSiteSettings() {
  const [entry] = await getCollection('settings');
  return entry.data;
}

import { defineCollection, reference, z } from 'astro:content';
import { glob } from 'astro/loaders';

const topicTag = z.enum(['Azure', 'AI', 'Power Platform', 'M365', '.NET', 'Community']);
const format = z.enum(['In-person', 'Virtual']);

const events = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/events' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    time: z.string(),
    tag: topicTag,
    format,
    location: z.string(),
    description: z.string(),
    meetupUrl: z.string().url(),
    image: z.string().optional(),
    agenda: z
      .array(
        z.object({
          time: z.string(),
          title: z.string(),
          speaker: z.string().optional(),
        })
      )
      .default([]),
    speakerIds: z.array(reference('speakers')).default([]),
    draft: z.boolean().default(false),
  }),
});

const speakers = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/speakers' }),
  schema: z.object({
    name: z.string(),
    title: z.string().optional(),
    photo: z.string().optional(),
    bio: z.string().optional(),
    linkedin: z.string().url().optional(),
    twitter: z.string().url().optional(),
  }),
});

const sponsors = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/sponsors' }),
  schema: z.object({
    name: z.string(),
    tier: z.enum(['platinum', 'gold', 'silver']),
    logo: z.string().optional(),
    link: z.string().url().optional(),
  }),
});

const videos = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/videos' }),
  schema: z.object({
    title: z.string(),
    youtubeId: z.string(),
    tag: topicTag,
    format: format.optional(),
    date: z.coerce.date().optional(),
    speakerId: reference('speakers').optional(),
    speakerName: z.string().optional(),
    eventId: reference('events').optional(),
    duration: z.string(),
  }),
});

const organizers = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/organizers' }),
  schema: z.object({
    name: z.string(),
    role: z.string(),
    order: z.number().default(0),
    photo: z.string().optional(),
    linkedin: z.string().url().optional(),
    twitter: z.string().url().optional(),
  }),
});

const sponsorTiers = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/sponsor-tiers' }),
  schema: z.object({
    label: z.string(),
    price: z.string(),
    order: z.number().default(0),
    featured: z.boolean().default(false),
    benefits: z.array(z.string()).default([]),
  }),
});

const highlights = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/highlights' }),
  schema: z.object({
    quote: z.string(),
    name: z.string(),
    role: z.string(),
    order: z.number().default(0),
  }),
});

const settings = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/settings' }),
  schema: z.object({
    memberCount: z.string(),
    eventsHosted: z.string(),
    speakersFeatured: z.string(),
  }),
});

export const collections = { events, speakers, sponsors, videos, organizers, settings, sponsorTiers, highlights };

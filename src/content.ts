export const site = {
  name: 'Art Engine',
  domain: 'artengine.lk',
  tagline: 'Sculpted light. Living walls.',
  subtagline: 'Custom wall features with warm LED glow — Halo niches, Wave shelves, and Modular systems. Designed, built & installed in Colombo + Gampaha.',
  whatsapp: {
    numberDisplay: '+94 76 992 6806',
    numberE164: '94769926806',
  },
  leadTime: '≈7 days (depending on design)',
  travelFeeGampaha: 'LKR 2,500',
};

export const nav = [
  { label: 'Home', href: '/' },
  { label: 'Products', href: '/products' },
  { label: 'Services', href: '/services' },
  { label: 'Gallery', href: '/gallery' },
  { label: 'Contact', href: '/contact' },
];

export type Product = {
  slug: string;
  name: string;
  series: 'Halo' | 'Wave' | 'Modular' | 'Botanical' | 'Light Art';
  priceFromLkr: number;
  leadTime?: string;
  image: string;
  description: string;
};

export const products: Product[] = [
  {
    slug: 'halo-niche',
    name: 'Halo Niche (LED Backlit)',
    series: 'Halo',
    priceFromLkr: 30000,
    image: '/images/product-01.jpg',
    description:
      'Circular/half-moon wall niche with warm LED glow. Designed to fit your wall and finished clean for a premium, zen look.',
  },
  {
    slug: 'arched-glow-panel',
    name: 'Arched Glow Panel (Vase Shelf)',
    series: 'Halo',
    priceFromLkr: 30000,
    image: '/images/product-23.jpg',
    description:
      'A signature Art Engine form: arched halo panel with a floating shelf + vase holder. Soft light, clean finish, strong presence.',
  },
  {
    slug: 'wave-shelf',
    name: 'Wave Shelf (Sculptural)',
    series: 'Wave',
    priceFromLkr: 25000,
    image: '/images/product-02.jpg',
    description:
      'Soft geometry shelf that looks like a sculpture. Minimal, functional, and designed for plants, vases, and objects.',
  },
  {
    slug: 'modular-shelves',
    name: 'Modular Shelves (Custom Layout)',
    series: 'Modular',
    priceFromLkr: 10000,
    image: '/images/product-03.jpg',
    description:
      'Geometric shelf modules arranged for your space. Perfect for modern living rooms and workspaces.',
  },
];

export const galleryImages = [
  '/images/product-04.jpg',
  '/images/product-05.jpg',
  '/images/product-06.jpg',
  '/images/product-07.jpg',
  '/images/product-08.jpg',
  '/images/product-09.jpg',
  '/images/product-10.jpg',
  '/images/product-11.jpg',
  '/images/product-12.jpg',
  '/images/product-13.jpg',
  '/images/product-14.jpg',
  '/images/product-15.jpg',
  '/images/product-16.jpg',
  '/images/product-17.jpg',
  '/images/product-18.jpg',
  '/images/product-19.jpg',
  '/images/product-20.jpg',
  '/images/product-21.jpg',
  '/images/product-22.jpg',
  '/images/product-23.jpg',
  '/images/product-24.jpg',
  '/images/product-25.jpg',
  '/images/product-26.jpg',
];

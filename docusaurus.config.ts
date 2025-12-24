import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Book',
  tagline: 'Learn to build intelligent robots',
  favicon: 'img/docusourus.jpg',

  customFields: {
    // API URL for the chatbot backend
    // Can be overridden by the RETRIEVAL_API_URL environment variable
    retrievalApiUrl: process.env.RETRIEVAL_API_URL || 'http://localhost:8000',
  },

  scripts: [
    {
      src: 'YOUR_CHATKIT_CDN_EMBED_SCRIPT_URL', // Replace with your actual ChatKit embed script URL
      async: true,
      defer: true,
    },
  ],

  // Set the production url of your site here
  url: 'https://Mutahir-15.github.io', // TODO: Update with your actual GitHub username
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/', // TODO: Adjust if deploying to a subpath

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Mutahir-15', // TODO: Update with your GitHub org/user name
  projectName: 'Physical-AI-Humanoid-Robotics-Textbook', // TODO: Update with your GitHub repo name

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',

          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/Physical-AI-Humanoid-Robotics-Textbook/tree/main/', // TODO: Update with your repo path
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/', // TODO: Update with your repo path
          // Configure onUntruncatedBlogPosts to ignore or warn if needed
          // onUntruncatedBlogPosts: 'warn', // or 'ignore'
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: '/img/docusaurus.jpg',
    navbar: {
      title: 'HUMA-ROBO',
      logo: {
        alt: 'Robotics Course Logo',
        src: 'img/docusaurus.jpg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'courseSidebar',
          position: 'left',
          label: 'Book',
        },
        {
          to: '/chat',
          label: 'Chat',
          position: 'left',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Book',
              to: '/',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/facebook/docusaurus', // TODO: Update with your GitHub repo
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} HUMA-ROBO, Inc. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

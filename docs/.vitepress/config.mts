import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'mnemosine',
  description: 'A schema-less SQLite storage library for larger projects: dynamic attributes, interconnected files, and vector search.',
  base: '/mnemosine/',
  lastUpdated: true,
  cleanUrls: true,

  themeConfig: {
    logo: {
      text: 'Mnemosine',
    },
    siteTitle: 'mnemosine',

    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'API Reference', link: '/storage/index' },
      { text: 'Architecture', link: '/guide/architecture' },
      {
        text: 'v0.1.0',
        items: [
          { text: 'Changelog', link: 'https://github.com/FrancoFantomius/mnemosine/blob/main/CHANGELOG.md' },
          { text: 'Releases', link: 'https://github.com/FrancoFantomius/mnemosine/releases' }
        ]
      }
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Introduction & Guides',
          items: [
            { text: 'Getting Started', link: '/guide/getting-started' },
            { text: 'Architecture & Design', link: '/guide/architecture' },
          ]
        },
        {
          text: 'Core Modules',
          items: [
            { text: 'Storage Engine', link: '/storage/index' },
            { text: 'Dynamic Nodes', link: '/node/index' },
            { text: 'Blob & File Store', link: '/file/index' },
            { text: 'Graph & Links', link: '/graph/index' },
            { text: 'Search & Vectors', link: '/search/index' },
          ]
        }
      ],
      '/': [
        {
          text: 'Guide',
          collapsed: false,
          items: [
            { text: 'Getting Started', link: '/guide/getting-started' },
            { text: 'Architecture', link: '/guide/architecture' },
          ]
        },
        {
          text: 'API Reference',
          collapsed: false,
          items: [
            { text: 'mnemosine.storage', link: '/storage/index' },
            { text: 'mnemosine.node', link: '/node/index' },
            { text: 'mnemosine.file', link: '/file/index' },
            { text: 'mnemosine.link', link: '/link/index' },
            { text: 'mnemosine.graph', link: '/graph/index' },
            { text: 'mnemosine.search', link: '/search/index' },
            { text: 'mnemosine.vec', link: '/vec/index' },
            { text: 'mnemosine.embed', link: '/embed/index' },
            { text: 'mnemosine.schema', link: '/schema/index' },
            { text: 'mnemosine.migrations', link: '/migrations/index' },
            { text: 'mnemosine.ids', link: '/ids/index' },
            { text: 'mnemosine.util', link: '/util/index' },
            { text: 'mnemosine.exceptions', link: '/exceptions/index' },
            { text: 'mnemosine (package)', link: '/package/index' },
          ]
        }
      ]
    },

    search: {
      provider: 'local'
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/FrancoFantomius/mnemosine' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 mnemosine contributors'
    },

    editLink: {
      pattern: 'https://github.com/FrancoFantomius/mnemosine/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    }
  }
})

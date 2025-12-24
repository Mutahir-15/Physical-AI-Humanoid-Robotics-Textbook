import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/blog',
    component: ComponentCreator('/blog', 'd10'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '182'),
    exact: true
  },
  {
    path: '/blog/tags',
    component: ComponentCreator('/blog/tags', '287'),
    exact: true
  },
  {
    path: '/blog/tags/docusaurus',
    component: ComponentCreator('/blog/tags/docusaurus', '6e8'),
    exact: true
  },
  {
    path: '/blog/tags/hello',
    component: ComponentCreator('/blog/tags/hello', 'a4a'),
    exact: true
  },
  {
    path: '/blog/tags/world',
    component: ComponentCreator('/blog/tags/world', '985'),
    exact: true
  },
  {
    path: '/blog/welcome',
    component: ComponentCreator('/blog/welcome', '6f2'),
    exact: true
  },
  {
    path: '/chat',
    component: ComponentCreator('/chat', '4b9'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'ee6'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '975'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'b01'),
            routes: [
              {
                path: '/docs/capstone',
                component: ComponentCreator('/docs/capstone', '983'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/capstone/evaluation',
                component: ComponentCreator('/docs/capstone/evaluation', '37d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/capstone/overview',
                component: ComponentCreator('/docs/capstone/overview', 'b3d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/chat/',
                component: ComponentCreator('/docs/chat/', '93c'),
                exact: true
              },
              {
                path: '/docs/contributing',
                component: ComponentCreator('/docs/contributing', '12c'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/contributing/style-guide',
                component: ComponentCreator('/docs/contributing/style-guide', 'de1'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/deployment/guide',
                component: ComponentCreator('/docs/deployment/guide', 'ae1'),
                exact: true
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '853'),
                exact: true
              },
              {
                path: '/docs/module1-ros2',
                component: ComponentCreator('/docs/module1-ros2', 'f5e'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module1-ros2/chapter1-introduction-to-ros2',
                component: ComponentCreator('/docs/module1-ros2/chapter1-introduction-to-ros2', 'c8e'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module1-ros2/chapter2-ros2-communication-patterns',
                component: ComponentCreator('/docs/module1-ros2/chapter2-ros2-communication-patterns', 'f5a'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module1-ros2/chapter3-ros2-services-actions',
                component: ComponentCreator('/docs/module1-ros2/chapter3-ros2-services-actions', '377'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module1-ros2/chapter4-robot-description-with-urdf',
                component: ComponentCreator('/docs/module1-ros2/chapter4-robot-description-with-urdf', 'd57'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module1-ros2/chapter5-simulation-instructions',
                component: ComponentCreator('/docs/module1-ros2/chapter5-simulation-instructions', 'af5'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module2-digital-twin',
                component: ComponentCreator('/docs/module2-digital-twin', '97d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module2-digital-twin/chapter1-advanced-urdf-sdf-modeling',
                component: ComponentCreator('/docs/module2-digital-twin/chapter1-advanced-urdf-sdf-modeling', '923'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module2-digital-twin/chapter2-gazebo-environment-physics',
                component: ComponentCreator('/docs/module2-digital-twin/chapter2-gazebo-environment-physics', '099'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module2-digital-twin/chapter3-ros2-gazebo-integration',
                component: ComponentCreator('/docs/module2-digital-twin/chapter3-ros2-gazebo-integration', 'd06'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module2-digital-twin/chapter4-unity-robot-model-import',
                component: ComponentCreator('/docs/module2-digital-twin/chapter4-unity-robot-model-import', '3d8'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module2-digital-twin/chapter5-unity-physics-sensors',
                component: ComponentCreator('/docs/module2-digital-twin/chapter5-unity-physics-sensors', '391'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module3-ai-brain',
                component: ComponentCreator('/docs/module3-ai-brain', '5fa'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module3-ai-brain/chapter1-isaac-sim-introduction',
                component: ComponentCreator('/docs/module3-ai-brain/chapter1-isaac-sim-introduction', 'ebf'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module3-ai-brain/chapter2-isaac-perception-tasks',
                component: ComponentCreator('/docs/module3-ai-brain/chapter2-isaac-perception-tasks', 'e64'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module3-ai-brain/chapter3-motion-planning-control',
                component: ComponentCreator('/docs/module3-ai-brain/chapter3-motion-planning-control', 'c16'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module3-ai-brain/chapter4-ros2-isaac-integration',
                component: ComponentCreator('/docs/module3-ai-brain/chapter4-ros2-isaac-integration', 'ba0'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module3-ai-brain/isaac-sim-architecture-diagram',
                component: ComponentCreator('/docs/module3-ai-brain/isaac-sim-architecture-diagram', 'dc6'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module3-ai-brain/motion-planning-workflow-diagram',
                component: ComponentCreator('/docs/module3-ai-brain/motion-planning-workflow-diagram', '519'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module3-ai-brain/perception-pipeline-diagram',
                component: ComponentCreator('/docs/module3-ai-brain/perception-pipeline-diagram', '1c3'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module4-vla',
                component: ComponentCreator('/docs/module4-vla', 'b6f'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module4-vla/chapter1-voice-llm-integration',
                component: ComponentCreator('/docs/module4-vla/chapter1-voice-llm-integration', '83a'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module4-vla/chapter2-natural-language-to-robot-actions',
                component: ComponentCreator('/docs/module4-vla/chapter2-natural-language-to-robot-actions', 'a01'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module4-vla/chapter3-combining-vision-language',
                component: ComponentCreator('/docs/module4-vla/chapter3-combining-vision-language', '6f4'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/module4-vla/chapter4-reactive-control-strategies',
                component: ComponentCreator('/docs/module4-vla/chapter4-reactive-control-strategies', '7bb'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/docs/rag_chatbot/chunking_strategy',
                component: ComponentCreator('/docs/rag_chatbot/chunking_strategy', 'cba'),
                exact: true
              },
              {
                path: '/docs/rag_chatbot/contextual_boundaries',
                component: ComponentCreator('/docs/rag_chatbot/contextual_boundaries', '8b9'),
                exact: true
              },
              {
                path: '/docs/rag_chatbot/db_schema',
                component: ComponentCreator('/docs/rag_chatbot/db_schema', '8f4'),
                exact: true
              },
              {
                path: '/docs/rag_chatbot/indexing_pipeline',
                component: ComponentCreator('/docs/rag_chatbot/indexing_pipeline', 'af9'),
                exact: true
              },
              {
                path: '/docs/rag_chatbot/vector_indexing',
                component: ComponentCreator('/docs/rag_chatbot/vector_indexing', '2b6'),
                exact: true
              },
              {
                path: '/docs/uat/uat-checklist',
                component: ComponentCreator('/docs/uat/uat-checklist', '809'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];

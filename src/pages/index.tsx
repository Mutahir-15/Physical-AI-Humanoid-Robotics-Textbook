import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import clsx from 'clsx'; // Import clsx for conditional class names
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Exploring the Course - 5min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageFeatures() {
  const features = [
    {
      title: 'Module 1: The Robotic Nervous System (ROS 2)',
      imageUrl: '/img/ros2-logo.png', // Placeholder
      description: (
        <>
          Dive into the fundamentals of ROS 2, learning how to build and orchestrate robot software.
        </>
      ),
      link: '/docs/module1-ros2',
    },
    {
      title: 'Module 2: The Digital Twin (Gazebo & Unity)',
      imageUrl: '/img/digital-twin-logo.png', // Placeholder
      description: (
        <>
          Create realistic digital twins of humanoid robots and simulate them in advanced environments.
        </>
      ),
      link: '/docs/module2-digital-twin',
    },
    {
      title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      imageUrl: '/img/isaac-sim-logo.png', // Placeholder
      description: (
        <>
          Integrate cutting-edge AI capabilities into your simulated humanoids using NVIDIA Isaac SDK.
        </>
      ),
      link: '/docs/module3-ai-brain', // Placeholder link
    },
    {
      title: 'Module 4: Vision-Language-Action (VLA Robotics)',
      imageUrl: '/img/vla-robotics-logo.png', // Placeholder
      description: (
        <>
          Connect vision, language, and action to enable intelligent, voice-commanded robot behaviors.
        </>
      ),
      link: '/docs/module4-vla', // Placeholder link
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {features.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

function Feature({imageUrl, title, description, link}) {
  const imgUrl = imageUrl;
  return (
    <div className={clsx('col col--3', styles.feature)}>
      {imgUrl && (
        <div className="text--center">
          <img className={styles.featureImage} src={imgUrl} alt={title} />
        </div>
      )}
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
        {link && <Link className="button button--primary" to={link}>Learn More</Link>}
      </div>
    </div>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <div className="container text--center margin-bottom--xl">
          <h2>Welcome to the Physical AI & Humanoid Robotics Course!</h2>
          <p>
            This course is designed to take you on a journey through the exciting world of
            physical AI and humanoid robotics. From foundational concepts in ROS 2 to
            advanced simulations in Gazebo and Unity, and integrating cutting-edge
            AI with NVIDIA Isaac, you will gain the skills to build and control
            intelligent robotic systems.
          </p>
          <p>
            Start by exploring our modules below to begin your learning adventure.
          </p>
        </div>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}

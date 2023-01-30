import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Built for teams',
    Svg: require('../../static/img/undraw_engineering_team.svg').default,
    description: (
      <>
        Spectra was designed for teams of teams and built for to work for any
        size organization quickly and easily.
      </>
    ),
  },
  {
    title: 'Focus on data',
    Svg: require('../../static/img/undraw_photo_session.svg').default,
    description: (
      <>
        Spectra helps you focus on data. Transform your organization with data-driven
        decision making at its core.
      </>
    ),
  },
  {
    title: 'Gain insights',
    Svg: require('../../static/img/undraw_financial_data.svg').default,
    description: (
      <>
        Analyze data, explore data anomalies, and gain actionable insights from
        a platform built for data science and analytics.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

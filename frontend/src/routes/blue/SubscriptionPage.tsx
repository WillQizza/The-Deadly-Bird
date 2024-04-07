import React, { useState } from 'react';
import { ReactComponent as Checkmark } from 'bootstrap-icons/icons/patch-check-fill.svg';
import Page from '../../components/layout/Page';
import styles from './SubscriptionPage.module.css'; 
import { Colors, publicDir } from '../../constants';

type SubscriptionType = "annual" | "monthly";

export const SubscriptionPage: React.FC = () => {
  const [paymentType, setPaymentType] = useState<SubscriptionType | "">("");
  const [isPaying, setIsPaying] = useState(false);

  const onSubscribe = () => {
    setIsPaying(true);
  };

  return <Page>
    <div id={styles.container}>
      <div id={styles.info}>
        <h1>Deadly Blue</h1>

        {/* Checkmark */}
        <div style={{
          height: 128,
          marginTop: 20,
          marginBottom: 20
        }}>
          <Checkmark style={{
            height: "100%",
            width: "100%",
            color: Colors.teal
          }} />
        </div>

        {/* Premium Description */}
        <div id={styles.premiumDescription}>
          <p>Elevate your social media journey with Deadly Blue, the premium subscription service by The Deadly Bird. Gain access to a world of exclusive benefits designed to enhance your online presence and engagement. Join today and redefine your experience!</p>
        </div>

        {/* Purchase Buttons */}
        <div id={styles.purchaseContainer}>
          <div 
            className={`${styles.purchaseOption} ${paymentType === 'annual' ? styles.active : ""} ${isPaying ? styles.disabled : ""}`}
            onClick={() => !isPaying && setPaymentType("annual")}
          >
            <h5>Annual Plan</h5>
            <span>CA$99.99 / year</span>
          </div>
          
          <div 
            className={`${styles.purchaseOption} ${paymentType === 'monthly' ? styles.active : ""} ${isPaying ? styles.disabled : ""}`}
            onClick={() => !isPaying && setPaymentType("monthly")}
          >
            <h5>Monthly Plan</h5>
            <span>CA$9.99 / month</span>
          </div>

          <div
            id={styles.purchaseButton} 
            className={paymentType === "" || isPaying ? styles.disabled : ""}
            onClick={onSubscribe}
          >
            <h5>Subscribe & Pay</h5>
          </div>
        </div>
      </div>

      <div id={styles.items}>
        <div className={styles.item} style={{ backgroundImage: `url("${publicDir}/static/premium/noads.png")` }}>
          <div className={styles.itemContent}>
            <h2>No Ads</h2>
          </div>
        </div>
        <div className={styles.item} style={{ backgroundImage: `url("${publicDir}/static/premium/noads.png")` }}>
          <div className={styles.itemContent}>
            <h2>Block Users</h2>
          </div>
        </div>
        <div className={styles.item} style={{ backgroundImage: `url("${publicDir}/static/premium/noads.png")` }}>
          <div className={styles.itemContent}>
            <h2>Stand Out</h2>
          </div>
        </div>
      </div>
    </div>
  </Page>;
};
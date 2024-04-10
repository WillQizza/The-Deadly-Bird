import React, { useEffect, useState } from 'react';
import { ReactComponent as XIcon } from 'bootstrap-icons/icons/x-lg.svg';
import Page from '../../components/layout/Page';
import styles from './SubscriptionPage.module.css'; 
import { Colors, publicDir } from '../../constants';
import { apiCheckSubscriptionStatus, apiGetSubscriptionURL } from '../../api/subscription';
import SubscriptionCheckmark from '../../components/subscription/Checkmark';
import { useSearchParams } from 'react-router-dom';

type SubscriptionType = "annual" | "monthly";

const SubscriptionPage: React.FC = () => {
  const [paymentType, setPaymentType] = useState<SubscriptionType | "">("");
  const [isPaying, setIsPaying] = useState(false);

  const [fetchedStatus, setFetchedStatus] = useState(false);
  const [isSubscribed, setSubscribed] = useState(false);

  const [ searchParams ] = useSearchParams();
  const [successPromptVisible, setSuccessPromptVisible] = useState(searchParams.has("success"));

  const onSubscribe = async () => {
    setIsPaying(true);
    const subscriptionURL = await apiGetSubscriptionURL(paymentType as SubscriptionType);
    window.location.href = subscriptionURL;
  };

  useEffect(() => {
    apiCheckSubscriptionStatus().then(status => {
      setSubscribed(status);
      setTimeout(() => setFetchedStatus(true), 5000);
    });
  }, []);

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
          <SubscriptionCheckmark style={{
            color: Colors.teal,
            cursor: "default"
          }} />
        </div>

        {/* Premium Description */}
        <div id={styles.premiumDescription}>
          <p>Elevate your social media journey with Deadly Blue, the premium subscription service by The Deadly Bird. Gain access to a world of exclusive benefits designed to enhance your online presence and engagement. Join today and redefine your experience!</p>
        </div>

        {/* Purchase Buttons */}
        <div id={styles.purchaseContainer}>
          {
            !isSubscribed
            ?
            <>
              <div 
                style={!fetchedStatus ? { cursor: "default" } : {}}
                className={`${styles.purchaseOption} ${paymentType === 'annual' ? styles.active : ""} ${isPaying ? styles.disabled : ""}`}
                onClick={() => fetchedStatus && !isPaying && setPaymentType("annual")}
              >
                <h5>Annual Plan</h5>
                <span>CA$99.99 / year</span>
              </div>
              
              <div 
                style={!fetchedStatus ? { cursor: "default" } : {}}
                className={`${styles.purchaseOption} ${paymentType === 'monthly' ? styles.active : ""} ${isPaying ? styles.disabled : ""}`}
                onClick={() => fetchedStatus && !isPaying && setPaymentType("monthly")}
              >
                <h5>Monthly Plan</h5>
                <span>CA$9.99 / month</span>
              </div>

              <div
                style={!fetchedStatus ? { cursor: "default" } : {}}
                id={styles.purchaseButton} 
                className={paymentType === "" || isPaying ? styles.disabled : ""}
                onClick={() => fetchedStatus && onSubscribe()}
              >
                <h5>Subscribe & Pay</h5>
              </div>
            </>
            : 
            <strong>You are already subscribed!</strong>
          }
        </div>
      </div>

      <div id={styles.items}>
        <div className={styles.item} style={{ backgroundImage: `url("${publicDir}/static/premium/noads.png")` }}>
          <div className={styles.itemContent}>
            <h2>No Ads</h2>
            <h4>Get rid of those pesky ads!</h4>
          </div>
        </div>
        <div className={styles.item} style={{ backgroundImage: `url("${publicDir}/static/premium/block.png")` }}>
          <div className={styles.itemContent}>
            <h2>Block Users</h2>
            <h4>Hide users from your feed!</h4>
          </div>
        </div>
        <div className={styles.item} style={{ backgroundImage: `url("${publicDir}/static/premium/bluecheckmark.png")` }}>
          <div className={styles.itemContent}>
            <h2>Stand Out</h2>
            <h4>Have a cool checkmark on your profile and posts!</h4>
          </div>
        </div>
      </div>
    </div>
    {
      successPromptVisible
      ?
      <>
        <div id={styles.successPrompt}>
          <XIcon style={{ float: "right", cursor: "pointer" }} onClick={() => setSuccessPromptVisible(false)} />
          <h1>Thank You!</h1>
          <div id={styles.successPromptImageContainer}>
            <SubscriptionCheckmark style={{ color: Colors.teal }} noLink />
          </div>
          <h3 id={styles.successPromptSubtitle}>You have now subscribed to Deadly Blue!</h3>
          <div id={styles.successPromptCompleteButton} onClick={() => setSuccessPromptVisible(false)}>
            Horray!
          </div>
        </div>
        <div id={styles.successOverlay} onClick={() => setSuccessPromptVisible(false)}></div>
      </>
      :
      null
    }
  </Page>;
};

export default SubscriptionPage;
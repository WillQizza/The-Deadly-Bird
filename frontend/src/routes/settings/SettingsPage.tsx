import { useEffect, useState } from "react";
import Page from "../../components/layout/Page";
import SettingsForm from "../../components/settings/SettingsForm";
import { apiGetAuthor } from "../../api/authors";
import { getUserId } from "../../utils/auth";
import { Author } from "../../api/types";

import styles from "./SettingsPage.module.css";

const SettingsPage: React.FC = () => {
  const [author, setAuthor] = useState<Author>();

  /** Gets user's profile information */
  useEffect(() => {
    apiGetAuthor(getUserId()).then(author => {
      if (author) {
        setAuthor(author);
      }
    });
  }, []);

  /** Settings page */
  return <Page selected="Settings">
    <div id={styles.container}>
      <div id={styles.content}>
        {/* Header Stats */}
        <div id={styles.header}>
          <div className={styles.headerItem}>
            <div>
              <span>Settings</span> <span className={styles.headerItemAmount}></span>
            </div>
          </div>
          <div className={styles.headerItem}>
            <div>
              <span>Posts</span> <span className={styles.headerItemAmount}>{author ? author.posts : ""}</span>
            </div>
          </div>
          <div className={styles.headerItem}>
            <div>
              <span>Following</span> <span className={styles.headerItemAmount}>{author ? author.following : ""}</span>
            </div>
          </div>
          <div className={styles.headerItem}>
            <div>
              <span>Followers</span> <span className={styles.headerItemAmount}>{author ? author.followers : ""}</span>
            </div>
          </div>
        </div>

        {/* Form */}
        <SettingsForm author={author} />

      </div>
    </div>
  </Page>;
};

export default SettingsPage;
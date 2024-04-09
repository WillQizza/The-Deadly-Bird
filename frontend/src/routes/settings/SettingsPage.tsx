import { useEffect, useState } from "react";
import Page from "../../components/layout/Page";
import SettingsForm from "../../components/settings/SettingsForm";
import { apiGetAuthor } from "../../api/authors";
import { getUserId } from "../../utils/auth";
import { Author } from "../../api/types";

import styles from "./SettingsPage.module.css";
import { Col, Row } from "react-bootstrap";

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
        <Row id={styles.header}>
          <Col className={styles.headerItem}>
            <span className = "posts-column">Posts</span> 
            <span className = "posts-number">{author ? author.posts : ""}</span>
          </Col>
          <Col className={styles.headerItem}>
            <span className = "following-column">Following</span> 
            <span className = "following-number">{author ? author.following : ""}</span>
          </Col>
          <Col className={styles.headerItem}>
            <span className = "followers-column">Followers</span> 
            <span className = "followers-number">{author ? author.followers : ""}</span>
          </Col>
        </Row>

        {/* Form */}
        <SettingsForm author={author} />

      </div>
    </div>
  </Page>;
};

export default SettingsPage;
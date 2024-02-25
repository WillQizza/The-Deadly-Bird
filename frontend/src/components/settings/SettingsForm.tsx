import { Button, Modal } from "react-bootstrap";
import styles from "./SettingsForm.module.css";
import SettingsInput from "./SettingsInput";
import React, { Fragment, useEffect, useState } from "react";
import { Author } from "../../api/types";
import { publicDir } from "../../constants";
import { apiRequest } from "../../utils/request";
import { baseURL } from "../../constants";
import { getUserId } from "../../utils/auth";

type SettingsFormOptions = {
  author?: Author;
};

const SettingsForm: React.FC<SettingsFormOptions> = ({ author }) => {
  const [profileImage, setProfileImage] = useState(`${publicDir}/static/default-avatar.png`);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [homeServer, setHomeServer] = useState("");
  const [password, setPassword] = useState("");
  const [bio, setBio] = useState("");
  const [loadedContent, setLoadedContent] = useState(false);

  const [showingAvatarModal, setShowingAvatarModal] = useState(false);
  const [avatarURL, setAvatarURL] = useState("");

  useEffect(() => {
    if (author) {
      setEmail(author.email!);
      setUsername(author.displayName);
      setHomeServer(author.host);
      setBio(author.bio);
      setLoadedContent(true);

      if (author.profileImage) {
        setProfileImage(author.profileImage);
      }
    }
  }, [author]);

  async function onSaveClicked(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const formData = new URLSearchParams({
      email,
      bio,
      profileImage,
      displayName: username
    })
    if (password !== "") {
      formData.append("password", password);
    }
  
    await apiRequest(`${baseURL}/api/authors/${getUserId()}/`, {
        method:"PUT",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
    });
  }


  function onAvatarPromptOpen() {
    setShowingAvatarModal(true);
    setAvatarURL("");
  }


  function onAvatarURLUploaded() {
    setProfileImage(avatarURL);
    setShowingAvatarModal(false);
  }

  return (
    <Fragment>
      <div id={styles.container}>
        <form method="POST" onSubmit={onSaveClicked}>
          <div className={styles.row}>
            {/* Avatar + Modifiable Information */}
            <div id={styles.avatarContainer} onClick={onAvatarPromptOpen}>
              <img alt="Profile Avatar" src={profileImage} />
            </div>
            <div style={{ flexGrow: 1 }}>
              <div className={styles.row}>  
                <SettingsInput title="Email" name="email" type="email" value={email} valueSetter={setEmail} disabled={!loadedContent} />
                <SettingsInput title="Username" name="username" type="text" value={username} valueSetter={setUsername} disabled={!loadedContent} />
              </div>
              <div className={styles.row}>
                <SettingsInput title="Home Server" name="homeserver" type="text" value={homeServer} disabled />
                <SettingsInput title="Password" name="password" type="password" value=""  valueSetter={setPassword} placeholder="*********" />
              </div>
            </div>
          </div>
          <div className={styles.row}>
            {/* Bio */}
            <SettingsInput title="Bio" name="bio" type="text" placeholder="What's on your mind?" value={bio} valueSetter={setBio} disabled={!loadedContent} />
          </div>

          <div className={styles.row} style={{ marginTop: 20, justifyContent: "flex-end" }}>
            <Button type="submit" size="lg" variant="info" disabled={!loadedContent} className={styles.saveChangesButton}>
                Save Changes
            </Button>
          </div>
        </form>
      </div>

      <Modal show={showingAvatarModal} centered={true} size="xl" style={{ width: "calc(100% - 14%)", marginLeft: "14%" }}>
        <Modal.Header closeButton onHide={() => setShowingAvatarModal(false)}>
          <Modal.Title>Avatar Upload</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <div id={styles.uploadModalBody}>
            <h4>Please provide the URL to the image you would like to upload</h4>
            <input id={styles.uploadImageUrlInput} name="url" type="text" value={avatarURL} onChange={e => setAvatarURL(e.currentTarget.value)} />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={onAvatarURLUploaded} disabled={avatarURL.length === 0}>Upload Avatar</Button>
        </Modal.Footer>
      </Modal>
    </Fragment>
  );
};

export default SettingsForm;
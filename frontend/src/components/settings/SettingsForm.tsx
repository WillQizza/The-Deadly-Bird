import { Button } from "react-bootstrap";
import styles from "./SettingsForm.module.css";
import SettingsInput from "./SettingsInput";
import React, { useEffect, useRef, useState } from "react";
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

  const avatarElement = useRef<HTMLInputElement>(null);

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
      displayName: username,
      email: email,
      bio: bio,
    })
    if (password !== "") {
      formData.append("password", password);
    }
  
    const response = await apiRequest(`${baseURL}/api/authors/${getUserId()}/`, {
        method:"PUT",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
    });
  }

  function onDeleteAccount(event: React.MouseEvent<HTMLButtonElement>) {

  }

  function onAvatarButtonClicked() {
    avatarElement.current!.click();
  }

  function onAvatarUploaded(event: React.ChangeEvent<HTMLInputElement>) {
    if (!event.target.files || !event.target.files[0]) {
      return;
    }

    const file = event.target.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    // handle the result
    reader.onload = () => {
      if (reader.result) {
        const b64Data = reader.result.toString();
        setProfileImage(b64Data);
      }
    };
  }

  return (
    <div id={styles.container}>
      <form method="POST" onSubmit={onSaveClicked}>
        <div className={styles.row}>
          {/* Avatar + Modifiable Information */}
          <div id={styles.avatarContainer} onClick={onAvatarButtonClicked}>
            <img alt="Profile Avatar" src={profileImage} />
            <input type="file" onChange={onAvatarUploaded} accept=",png,.jpeg,.jpg" ref={avatarElement} style={{ display: "none" }} />
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
          <Button variant="danger" size="lg" disabled={!loadedContent} onClick={onDeleteAccount}>
              Delete Account
          </Button>
          <Button type="submit" size="lg" variant="info" disabled={!loadedContent} className={styles.saveChangesButton}>
              Save Changes
          </Button>
        </div>
      </form>
    </div>
  );
};

export default SettingsForm;
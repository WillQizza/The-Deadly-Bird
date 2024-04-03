import { Button, Form, Image, Modal } from "react-bootstrap";
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
  const [displayName, setDisplayName] = useState("");
  const [homeServer, setHomeServer] = useState("");
  const [password, setPassword] = useState("");
  const [bio, setBio] = useState("");
  const [github, setGithub] = useState("");
  const [loadedContent, setLoadedContent] = useState(false);

  const [showingAvatarModal, setShowingAvatarModal] = useState(false);
  const [avatarURL, setAvatarURL] = useState("");

  const [formErrors, setFormErrors] = useState<{ [key: string]: string }>({});

  /** Get's the user's profile information */
  useEffect(() => {
    if (author) {
      setEmail(author.email!);
      setDisplayName(author.displayName);
      setHomeServer(author.host);
      setBio(author.bio);
      setGithub((author.github || "").substring("https://github.com/".length));
      setLoadedContent(true);

      if (author.profileImage) {
        setProfileImage(author.profileImage);
      }
    }
  }, [author]);

  /** Function to handle profile save */
  async function onSaveClicked(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (validateForm()) {
      // Send request to update profile
      const formData = new URLSearchParams({
        email,
        bio,
        profileImage,
        github,
        displayName: displayName
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

      // Return to profile page
      window.location.href = "/profile";
    }
  }

  /** Function for validating form input */
  const validateForm = () => {
    let isValid = true;
    const newFormErrors: { [key: string]: string } = {};

    if (!email) {
      isValid = false;
      newFormErrors['email'] = 'Email is required';
    }
    if (email.length > 255) {
      isValid = false;
      newFormErrors['email'] = 'Email is too long (255 characters maximum)';
    }
    if (!displayName) {
      isValid = false;
      newFormErrors['displayName'] = 'Display name is required';
    }
    if (displayName.length > 255) {
      isValid = false;
      newFormErrors['displayName'] = 'Display name is too long (255 characters maximum)'
    }
    if (!password) {
      isValid = false;
      newFormErrors['password'] = 'Password is required';
    }

    setFormErrors(newFormErrors);
    return isValid;
  };

  /** Function to handle avatar prompt opened */
  function onAvatarPromptOpen() {
    setShowingAvatarModal(true);
    setAvatarURL("");
  }

  /** Function to handle avatar url upload */
  function onAvatarURLUploaded() {
    setProfileImage(avatarURL);
    setShowingAvatarModal(false);
  }

  /** Settings form */
  return (
    <>
      <Fragment>
        <div id={styles.container}>
          {/** Form */}
          <Form method="POST" onSubmit={onSaveClicked}>
            {/* Avatar */}
            <div id={styles.avatarContainer}>
              <Image
                id={styles.avatar}
                src={profileImage}
                alt={"Profile Avatar"}
                onClick={onAvatarPromptOpen}
                roundedCircle
              />
            </div>
            {/** Email */}
            <SettingsInput
              title="Email"name="email" type="email"
              value={email} valueSetter={setEmail} disabled={!loadedContent}
              formErrors={formErrors} formErrorKey="email"
            />
            {/** Display name */}
            <SettingsInput
              title="Display Name" name="displayName" type="text"
              value={displayName} valueSetter={setDisplayName} disabled={!loadedContent}
              formErrors={formErrors} formErrorKey="displayName"
            />
            {/** Home server */}
            <SettingsInput
              title="Home Server"
              name="homeserver"
              type="text" 
              value={homeServer} disabled
            />
            {/** Password */}
            <SettingsInput
              title="Password" name="password" type="password"
              value="" valueSetter={setPassword} placeholder="*********"
              formErrors={formErrors} formErrorKey="password"
            />
            {/** Bio */}
            <SettingsInput
              title="Bio" name="bio" type="text" placeholder="What's on your mind?"
              value={bio} valueSetter={setBio} disabled={!loadedContent}
            />
            {/** Github */}
            <SettingsInput
              title="Github" name="github" type="text"
              value={github} valueSetter={setGithub} disabled={!loadedContent}
            />
            {/** Save changes button */}
            <Button 
              type="submit" disabled={!loadedContent} 
              className={styles.saveChangesButton}
            >
              Save Changes
            </Button>
          </Form>
        </div>
      </Fragment>
      {/** Avatar upload modal */}
      <Modal
      show={showingAvatarModal}
      onHide={() => setShowingAvatarModal(false)}
      size={"lg"}
      centered
      id={styles.uploadModal}
      data-bs-theme="dark"
      >
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
    </>
  );
};

export default SettingsForm;
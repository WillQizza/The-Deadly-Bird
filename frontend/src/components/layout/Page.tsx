import React, { useState } from "react";
import styles from "./Page.module.css";
import Footer from "./Footer";
import { Offcanvas } from 'react-bootstrap';
import Inbox from "../inbox/Inbox";
import Navigation, { SelectedNavigation } from "./Navigation";
import { useNavigate } from "react-router-dom";
import { ReactComponent as House } from 'bootstrap-icons/icons/house.svg';
import { ReactComponent as Person } from 'bootstrap-icons/icons/person.svg';
import { ReactComponent as Globe } from 'bootstrap-icons/icons/globe.svg';
import { ReactComponent as Gear } from 'bootstrap-icons/icons/gear.svg';
import { ReactComponent as Star } from 'bootstrap-icons/icons/star-fill.svg';
import { setUserId } from "../../utils/auth";
import { apiRequest } from "../../utils/request";
import { baseURL } from "../../constants";
import { ReactComponent as InboxIcon } from 'bootstrap-icons/icons/inboxes-fill.svg';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Page = ({ children, selected, overflowScrollOff } : { children: React.ReactNode, selected?: SelectedNavigation, overflowScrollOff?: Boolean }) => {
     
    const [showSidebar, setShowSidebar] = useState(false);
    const toggleSidebar = () => setShowSidebar(!showSidebar);
    const navigate = useNavigate();

    /** Function handling logout */
    const logOut = () => {
        setUserId(null);
        apiRequest(`${baseURL}/api/logout/`, { method: "POST" });
        navigate("/");
    };

    /** Page */
    return (
        <div id={styles.root}>
            <div id={styles.contentRoot}>
                {/** Navigation bar */}
                <Navigation items={[
                    { name: "Home", icon: <House />, path: "/home" },
                    { name: "Profile", icon: <Person />, path: "/profile" },
                    { name: "Network", icon: <Globe />, path: "/network" },
                    { name: "Premium", icon: <Star />, path: "/subscription" },
                    { name: "Settings", icon: <Gear />, path: "/profile/settings" },
                ]} selected={selected} />
                {/** Content */}
                <div id={styles.contentAndUpperNav}>
                    {/** Toolbar containing inbox and logout buttons */}
                    <div id={styles.thinNavbar}>

                        <div className={styles.inboxButtonContainer}
                            onClick={() => {toggleSidebar()}} 
                        >
                            <InboxIcon className={styles.inboxButton}/>
                            Inbox
                        </div>  

                        <button onClick={() => {logOut()}}>Log Out</button>
                    </div>
                    {/** Page content */}
                    <div className={`${styles.content} ${!overflowScrollOff ? styles.overflowScroll : ''}`}>
                        <ToastContainer
                            position="top-right"
                            theme="dark"
                            autoClose={2500}
                        />
                        {children}
                    </div>
                </div>
            </div>
            {/** Inbox */}
            <Offcanvas show={showSidebar} onHide={() => {setShowSidebar(false);}} placement="end" data-bs-theme="dark">
                <Offcanvas.Header closeButton>
                    <Offcanvas.Title>Inbox</Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>
                    <Inbox></Inbox>
                </Offcanvas.Body>
            </Offcanvas>
            <Footer />
        </div>
    );
};

export default Page;

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
import { setUserId } from "../../utils/auth";
import { apiRequest } from "../../utils/request";
import { baseURL } from "../../constants";

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
                <div id={styles.navigation}>
                    <Navigation items={[
                        { name: "Home", icon: House, path: "/home" },
                        { name: "Profile", icon: Person, path: "/profile" },
                        { name: "Network", icon: Globe, path: "/network" },
                        { name: "Settings", icon: Gear, path: "/profile/settings" }
                    ]} selected={selected} />
                </div>
                <div id={styles.contentAndUpperNav}>
                    {/** Toolbar containing inbox and logout buttons */}
                    <div id={styles.thinNavbar}>
                        <button onClick={() => {toggleSidebar()}}>Inbox</button>
                        <button onClick={() => {logOut()}}>Log Out</button>
                    </div>
                    {/** Page content */}
                    <div className={`${styles.content} ${!overflowScrollOff ? styles.overflowScroll : ''}`}>
                        {children}
                    </div>
                </div>
            </div>
            {/** Inbox */}
            <Offcanvas show={showSidebar} onHide={() => {setShowSidebar(false);}} placement="end">
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

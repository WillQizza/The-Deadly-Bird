import React, { useState } from 'react';
import { publicDir } from "../../constants";
import styles from "./Navigation.module.css";
import { ReactComponent as CreatePost } from 'bootstrap-icons/icons/plus-circle.svg';
import { ReactComponent as ArrowLeft } from 'bootstrap-icons/icons/arrow-left.svg';
import { ReactComponent as List } from 'bootstrap-icons/icons/list.svg';
import { Link, useNavigate } from 'react-router-dom';
import { Sidebar, Menu, MenuItem, SubMenu } from 'react-pro-sidebar';
import { Button } from 'react-bootstrap';

type NavItem = {
    name: string;
    path: string;
    icon: React.ReactNode;
};

export type SelectedNavigation = "Home" | "Profile" | "Network" | "Settings" | "Premium";


const Navigation = ({ items, selected }: { items: NavItem[], selected?: SelectedNavigation }) => {
    
    const [collapsed, setCollapsed] = useState(true);

    /** Navigation bar */
    return (
        <>
            <Sidebar
                id={styles.sidebar}
                collapsed={collapsed}
            >
                {/** Header (logo and navbar button) */}
                {(collapsed) ? (
                    <div id={styles.sidebarHeaderCollapsed}>
                        <img src={`${publicDir}/static/small-logo.png`} alt="Logo" />
                        <Button
                            id={styles.sidebarBtnCollapsed}
                            variant={"outline-light"}
                            onClick={() => setCollapsed(!collapsed)}
                        >
                            <List/>
                        </Button>
                    </div>
                ) : (
                    <div id={styles.sidebarHeader}>
                        <Button
                            id={styles.sidebarBtn}
                            variant={"outline-light"}
                            onClick={() => setCollapsed(!collapsed)}
                        >
                            <ArrowLeft/>
                        </Button>
                        <img src={`${publicDir}/static/small-logo.png`} alt="Logo" />
                    </div>
                )}
                {/** Menu */}
                <Menu>
                    {/** Add post button */}
                    <MenuItem
                        id={styles.createPostBtn}
                        icon={<CreatePost/>}
                        component={<Link to={"/post"} />}
                    >
                        Create Post
                    </MenuItem>
                    {/** Navigation links */}
                    {items.map((item, index) => (
                        <MenuItem
                            icon={item.icon}
                            component={<Link to={item.path} />}
                            className={`${styles.menuItem} ${selected === item.name ? styles.selectedMenuItem : null}`}
                        >
                            {item.name}
                        </MenuItem>
                    ))}
                </Menu>
            </Sidebar>
        </>
    ); 
};

export default Navigation;

import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer className="footer">
            <div className="footerContainer">
                <span>&copy; {new Date().getFullYear()} The Deadly Bird</span>
            </div>
        </footer>
    );
};

export default Footer;

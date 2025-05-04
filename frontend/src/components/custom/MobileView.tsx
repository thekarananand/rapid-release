import css from "./MobileView.module.scss";

const MobileView = () => {
    return (
        <main className={ css.main }>
            <div className={ css.error }>
        
                <h1>
                    Hey champ! <br/>
                    Rapid Release is built for big screens. 🚀
                </h1>
                <div>
                    Bring out the desktop, we’ll be waiting. 💻
                </div>
        
            </div>
        </main>
    );
};

export default MobileView;

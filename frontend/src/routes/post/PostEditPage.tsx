import styles from './PostEditPage.module.css';
import Page from '../../components/layout/Page';
import PostForm from '../../components/post/PostForm';
import { useParams } from 'react-router-dom';

const PostEditPage: React.FC = () => {
    const params = useParams();
    const postId = params['id'] || '';

    /** Post edit page */
    return (
        <Page>
            <div className={styles.postEditContentContainer}>
                <h1 className={styles.pageTitle}>Edit Your Post</h1>
                <PostForm postId={postId} edit={true}/>
            </div>
        </Page>
    );
}

export default PostEditPage;
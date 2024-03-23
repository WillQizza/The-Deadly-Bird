import { Modal, Button } from "react-bootstrap";
import { apiDeletePosts } from "../../api/posts";
import { getUserId } from "../../utils/auth";
import { useNavigate } from "react-router-dom";

interface DeleteDialogProps {
    show: boolean,
    setShow: React.Dispatch<React.SetStateAction<boolean>>,
    postId: string,
    onDelete?: () => void;  // function for additional delete handling 
}

const DeleteDialog: React.FC<DeleteDialogProps> = (props: DeleteDialogProps) => {
    const { show, setShow, postId, onDelete = () => {} } = props;
    const navigate = useNavigate();
    
    /** Function called from delete button to remove the local post*/
    const handleDeletePost = async () => {
     
        console.log("delete post:", postId);
        await apiDeletePosts(getUserId(), postId)
            .then(response => {
                if (response.status == 204) {

                    navigate("/home");
                } else if (response.status == 404) {
                    alert("Post not found");
                } else if (response.status == 500) {
                    alert("Failed to delete: Internal server error");
                }
            });
        setShow(false);
        onDelete();
    }

    /** Function rendering confirmation dialog upon post deletion */
    return (
        <Modal show={show} onHide={() => {setShow(false)}} data-bs-theme={"dark"}>
            <Modal.Header closeButton>
                <Modal.Title className={"text-white"}>Delete Post</Modal.Title>
            </Modal.Header>
            <Modal.Body className={"text-white"}>Are you sure you want to delete this post?</Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => {setShow(false)}}>
                    Cancel
                </Button>
                <Button variant="danger" onClick={handleDeletePost}>
                    Delete
                </Button>
            </Modal.Footer>
        </Modal>
    );
}

export default DeleteDialog;
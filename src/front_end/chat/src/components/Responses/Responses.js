import List from '@mui/material/List';
import { ListItem } from '@mui/material';
import ListItemText from '@mui/material/ListItemText';

const Responses = ({ responses }) => {

    // Building HTML
    return (
        <List>
            {
                responses.map((response) => (
                    <ListItem>
                        <ListItemText 
                            primary={response} 
                            secondary={ response === responses[0] ? "Selected Response" : "Candidate Response" } />
                    </ListItem>
                ))
            }
        </List>
    )
}

export default Responses

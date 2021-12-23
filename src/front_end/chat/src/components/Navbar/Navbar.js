import { AppBar, Typography } from "@material-ui/core";
import useStyles from './styles'

const Navbar = () => {
    const classes = useStyles();

    const members = `Farjad Ilyas 18I-0436\nNabeel Danish 18I-0579\nSaad Saqlain 18I-0694`

    // Building HTML
    return (
        <AppBar className={classes.appBar} position='static' color="inherit">
            <div className={classes.brandContainer}>
                <Typography className={classes.heading} variant="h2" align="center">MUKALMA</Typography>
                <Typography variant="overline" display="block" gutterBottom className={classes.Members}>
                    {members}
                </Typography>
            </div>
        </AppBar>
    )
}

export default Navbar

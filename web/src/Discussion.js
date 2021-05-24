const Discussion = (props) =>
{
    return (
        <li key={props.data}>
            (<strong>
                {props.data.days_ago >= 365 ? Math.floor(props.data.days_ago / 365) + " years" : props.data.days_ago + " days"}
            </strong> ago) &nbsp;
            <a href={props.data.url}>{props.data.title}</a>
            &nbsp;
            ({props.data.game_name} - {props.data.num_replies} replies)
        </li>
    )
}

export default Discussion;
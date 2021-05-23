const Review = (props) =>
{
    return (
        <div key={props.data.recommendationId}>
            <p><strong>{props.data.voted_up ? "Positive" : "Negative"} </strong>
            reviewed for <strong>{props.data.title} </strong>
            as of <strong>{props.data.days_ago >= 365 ? Math.floor(props.data.days_ago / 365) + " years" : props.data.days_ago + " days"}</strong> ago:</p>
            <p>{props.data.review}</p>
 
           <hr />

        </div>
    )
}

export default Review;
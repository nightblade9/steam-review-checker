const Review = (props) =>
{
    return (
        <div key={props.data.recommendationId}>
            <p>Reviewed <strong>{props.data.days_ago}</strong> days ago:</p>
            <p>{props.data.review}</p>
 
           <hr />

        </div>
    )
}

export default Review;
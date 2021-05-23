const Review = (props) =>
{
    const STEAM_APP_URL = "https://store.steampowered.com/app"; // append app_id
    const STEAM_GAME_URL = STEAM_APP_URL + "/" + props.data["app_id"];
    const REVIEW_TYPE = props.data.voted_up ? "Positive" : "Negative";

    return (
        
        <div key={props.data.recommendationId}>
            <p><strong class={REVIEW_TYPE}>{REVIEW_TYPE}</strong>&nbsp;
            review for <a href={STEAM_GAME_URL}>{props.data.title}</a><span> </span>
            as of <strong>{props.data.days_ago >= 365 ? Math.floor(props.data.days_ago / 365) + " years" : props.data.days_ago + " days"}</strong> ago:</p>
            <p class="reviewText">{props.data.review}</p>
 
           <hr />

        </div>
    )
}

export default Review;
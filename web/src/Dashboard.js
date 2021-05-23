import React, { useEffect, useState } from 'react';
import Review from './Review'

export const Dashboard = () =>
{
    const [reviews, setReviews] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            fetch("data/reviews.json", {
                "headers": {
                "Content-Type": "application/json"
            }})
            .then(response => response.json())
            .then(data => {
                console.log(data);
                setReviews(data);
            });
        }

        if (reviews.length === 0)
        {
            fetchData();
        }
    });

    return (
        <div id="dashboard">
            <p>{reviews.length} reviews:</p>
                {reviews.map(review =>
                    // TODO: move into review child component
                    <Review data={review} />
                )}
        </div>
    )
}
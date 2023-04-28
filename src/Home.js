
import React, { Component } from 'react'
import axios from 'axios';
import { ConstructionOutlined } from '@mui/icons-material';
import { useEffect, useState } from 'react';
import SearchBar from './SearchBar';

export default function Home() {
    const [predicted, setPredicted] = useState([]);
    const [params, setParams] = useState({});
    useEffect(() => {
        getPredicted(params, setPredicted);
    }, [params]);

    const getPredicted = async (params, setPredicted) => {
        try {


            const response = await axios.get(`http://localhost:4242`, {
                params: {
                    stockName: params.stockName,
                    period: params.period,
                    interval: params.interval,
                    openPrice: params.openPrice,
                    low: params.low,
                    high: params.high,
                    volume: params.volume
                }

            });

            const predicted = response.data;
            console.log("Pred:", predicted)
            setPredicted(predicted);

        } catch (error) {
            console.log(error)
            setPredicted(0);
        }
    }
    return (
        <div align='center'>
            <SearchBar params={params} setParams={setParams} />


            The predicted value of this stock is {predicted}.
        </div>
    );
}



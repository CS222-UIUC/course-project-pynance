
import React from 'react'
import { useState } from 'react';
import { Box, TextField, Button, Select, MenuItem } from '@mui/material';
// import { Form, FormControl, FormLabel, Dropdown } from "react-bootstrap";
function SearchBar(props) {
    const [stockName, setStockName] = useState(props.params.stockName);
    const [period, setPeriod] = useState(props.params.period);
    const [interval, setInterval] = useState(props.params.interval);
    const [openPrice, setOpenPrice] = useState(props.params.openPrice);
    const [low, setLow] = useState(props.params.low);
    const [high, setHigh] = useState(props.params.high);
    const [volume, setVolume] = useState(props.params.volume);
    const handleSubmit = (e) => {
        e.preventDefault();
        props.setParams({ ...props.params, stockName: stockName, period: period, interval: interval, openPrice: openPrice, low: low, high: high, volume: volume });
    }

    return (

        <Box
            sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                gap: 1,
            }}
        >
            <TextField
                label="Enter Stock Name"
                variant="outlined"
                value={stockName}
                onChange={(event) => setStockName(event.target.value)}
            />
            <TextField
                label="Enter Stock Period"
                variant="outlined"
                value={period}
                onChange={(event) => setPeriod(event.target.value)}
            />
            <TextField
                label="Enter Stock Interval"
                variant="outlined"
                value={interval}
                onChange={(event) => setInterval(event.target.value)}
            />
            <TextField
                label="Enter Opening Price"
                variant="outlined"
                value={openPrice}
                onChange={(event) => setOpenPrice(event.target.value)}
            />
            <TextField
                label="Enter Low"
                variant="outlined"
                value={low}
                onChange={(event) => setLow(event.target.value)}
            />
            <TextField
                label="Enter High"
                variant="outlined"
                value={high}
                onChange={(event) => setHigh(event.target.value)}
            />
            <TextField
                label="Enter Volume"
                variant="outlined"
                value={volume}
                onChange={(event) => setVolume(event.target.value)}
            />

            <Button variant="contained" onClick={handleSubmit}>
                Search
            </Button>
        </Box>
    )
}

export default SearchBar
import React from 'react'
import { classnames } from '../utils/general'


const CustomInput = ({ customInput, setCustomInput }) => {
    return (
        <>
            {" "}
            <textarea

                rows="5"
                value={customInput}
                onChange={(e) => setCustomInput(e.target.value)}
                placeholder="Custom Input / This window will be available later, currently the war is on with Docker)"
            ></textarea>
        </>
    )
}

export default CustomInput;

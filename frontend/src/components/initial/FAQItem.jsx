import { useState } from "react";

const FAQItem = (props) => {
    const {
        question,
        answer,
    } = props
        const [isOpen, setIsOpen] = useState(false);

        const changeItemVisibility = () => {
            setIsOpen(!isOpen);
            console.log(isOpen)
        }


    return (
        <div className="faq-item">

    <h3 onClick={changeItemVisibility}>
        {isOpen ? "▼" : "▶"} {question}
    </h3>

    {isOpen && <p>{answer}</p>}

</div>
    )
}

export default FAQItem;
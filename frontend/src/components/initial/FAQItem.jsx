import { useState } from "react";

const FAQItem = (props) => {
    const {
        question,
        answer,
    } = props
        const [isOpen, setIsOpen] = useState(false);

        const changeItemVisibility = () => setIsOpen((value) => !value);


    return (
        <div className="faq-item">

    <h3>
        <button type="button" aria-expanded={isOpen} onClick={changeItemVisibility}>
          <span aria-hidden="true">{isOpen ? "−" : "+"}</span>
          {question}
        </button>
    </h3>

    {isOpen && <p>{answer}</p>}

</div>
    )
}

export default FAQItem;

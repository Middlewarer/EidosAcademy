const Button = (props) => {
    const {
        children,
        className = "",
        type='button',
        onClick,
    } = props

    return (
        <button className={`learning-button ${className}`.trim()} type={type} onClick={onClick}>
            {children}
          </button>
    )
}

export default Button;

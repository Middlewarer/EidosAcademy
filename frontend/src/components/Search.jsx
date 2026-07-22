const Search = (props) => {
    const {
        className='courses-search',
        type='text',
        placeholder="Поиск курса...",
        setSearch,
    } = props
    return (<div className={`${className}`}>
              <input
                type={type}
                placeholder={placeholder}
                onChange={(event) => {setSearch(event.target.value)}}
              />
            </div>)
}

export default Search
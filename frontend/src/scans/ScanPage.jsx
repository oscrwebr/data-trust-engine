function ScanPage({}) {

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [scan, setScan] = useState(null);

    // Get scan details through ID
    useEffect(() => {
        api.get("/scanning/get_scan_by_id")
        .then(response => {
            setLoading(false);
            setScan(response.data);
        })
        .catch(error => {
            console.error("Error fetching scan:", error);
            setError(error);
            setLoading(false);
        })
    }, [])

    return (
        <div className="scan-header">
            <h1 className="scan-heading">Scan {scan.scan_id}</h1>
            <Divider/>
        </div>
    )
}

export default ScanPage;
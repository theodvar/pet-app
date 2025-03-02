--
-- PostgreSQL database cluster dump
--

-- Started on 2025-03-02 17:28:35

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2025-03-02 17:28:35

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2025-03-02 17:28:35

--
-- PostgreSQL database dump complete
--

--
-- Database "pets_db" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2025-03-02 17:28:35

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5732 (class 1262 OID 16384)
-- Name: pets_db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE pets_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Greek_Greece.1253';


ALTER DATABASE pets_db OWNER TO postgres;

\connect pets_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 16385)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 5733 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 226 (class 1259 OID 17631)
-- Name: dogparks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dogparks (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    geometry public.geometry NOT NULL,
    location text,
    city character varying(100),
    comment text,
    image bytea
);


ALTER TABLE public.dogparks OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17630)
-- Name: dogparks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dogparks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dogparks_id_seq OWNER TO postgres;

--
-- TOC entry 5734 (class 0 OID 0)
-- Dependencies: 225
-- Name: dogparks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dogparks_id_seq OWNED BY public.dogparks.id;


--
-- TOC entry 228 (class 1259 OID 17640)
-- Name: dogwalks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dogwalks (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    geometry public.geometry NOT NULL,
    location text,
    city character varying(100),
    comment text,
    image bytea
);


ALTER TABLE public.dogwalks OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17639)
-- Name: dogwalks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dogwalks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dogwalks_id_seq OWNER TO postgres;

--
-- TOC entry 5735 (class 0 OID 0)
-- Dependencies: 227
-- Name: dogwalks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dogwalks_id_seq OWNED BY public.dogwalks.id;


--
-- TOC entry 224 (class 1259 OID 17622)
-- Name: petspointofinterest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.petspointofinterest (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    category character varying(100),
    geometry public.geometry NOT NULL,
    address text,
    city character varying(100),
    comment text,
    image bytea
);


ALTER TABLE public.petspointofinterest OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17621)
-- Name: petspointofinterest_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.petspointofinterest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.petspointofinterest_id_seq OWNER TO postgres;

--
-- TOC entry 5736 (class 0 OID 0)
-- Dependencies: 223
-- Name: petspointofinterest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.petspointofinterest_id_seq OWNED BY public.petspointofinterest.id;


--
-- TOC entry 5560 (class 2604 OID 17634)
-- Name: dogparks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dogparks ALTER COLUMN id SET DEFAULT nextval('public.dogparks_id_seq'::regclass);


--
-- TOC entry 5561 (class 2604 OID 17643)
-- Name: dogwalks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dogwalks ALTER COLUMN id SET DEFAULT nextval('public.dogwalks_id_seq'::regclass);


--
-- TOC entry 5559 (class 2604 OID 17625)
-- Name: petspointofinterest id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.petspointofinterest ALTER COLUMN id SET DEFAULT nextval('public.petspointofinterest_id_seq'::regclass);


--
-- TOC entry 5724 (class 0 OID 17631)
-- Dependencies: 226
-- Data for Name: dogparks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dogparks (id, title, geometry, location, city, comment, image) FROM stdin;
15	Πάρκο Πλατεία Οβρένοβιτς	0103000020E61000000100000006000000DC503F7115B83740186B8BBF36FA4240193B4FFA36B8374056E9CEA829FA4240A7DB593A4CB83740C48E44C631FA4240F9FD470928B83740CAD981FE3EFA424038DA4C8B13B837401CA3E36A37FA4240DC503F7115B83740186B8BBF36FA4240	Κριναγόρου 11,  117 45	Athens	700 τετραγωνικά πάρκο στο Νεο Κόσμο. Πλήρως εξοπλισμένο.	\N
8	Dog Park Παραλιακή	0103000020E61000000100000005000000761A69A9BC1D39402FF2576DA3AB414040ED0104BD1D39404413CDA89EAB4140BE463767E91D3940BA579C20A0AB4140F5A7E8A3E71D394011493EC0A4AB4140761A69A9BC1D39402FF2576DA3AB4140	Λεωφ. Σοφοκλή Βενιζέλου, Ηράκλειο 713 03	Heraklion	Μικρό πάρκο, δίπλα στη θάλασσα	\N
10	Πάρκο Σκύλων Άλσος Προμπονά	0103000020E61000000100000007000000B7613C4ED1BD374008DF6A0BF9034340345287D9C3BD37403CCBEEEDED0343408DECF50DCCBD3740D41FC1B2EA034340D49244F6D1BD3740541C9470EA0343407983E3C6DDBD3740BC6D7F41F00343407983E3C6DDBD374074CBDAB7F6034340B7613C4ED1BD374008DF6A0BF9034340	Ερατωνος 2, Αθήνα 111 43	Athens	Οργανωμένο πάρκο σκύλων, με 2 ξεχωριστούς χώρους για μικρόσωμα και μεγαλόσωμα σκυλάκια. Εφοδιασμένο με παιχνίδια agility, νερό. Κατάλληλο για την εκτόνωση και την κοινωνικοποίηση του σκύλου μας :)	\N
1	Πάρκο Αγίας Ελεούσης	0103000020E61000000100000006000000265C23DD2AB13740FE27243E1CFA4240145A773A34B137405C2C07FC17FA4240995544F23AB137402ED9565815FA4240A0D33DFC46B137405032EF2719FA42402BDA1CE736B13740C835BBA420FA4240265C23DD2AB13740FE27243E1CFA4240	Αγίας Ελεούσης 36, Καλλιθέα 176 75	Athens	Καθαρό, περιφραγμένο αλλά μικρό πάρκο!	\N
3	Πάρκο Χωροφυλακής	0103000020E6100000010000000B0000000AF8359204C53740B360E28FA2FE4240833B061A22C537400F73936291FE42401442621635C5374038E9C77086FE42407A617CE24AC53740173F32C280FE4240E6BF513C78C5374070E998F38CFE424012DBDD0374C537406C83C94395FE424098970D7C56C537407B60110D9CFE42404F7A3AB24DC537403A668F06A6FE4240D12F004345C53740B8205B96AFFE4240F73F1B1428C5374060234910AEFE42400AF8359204C53740B360E28FA2FE4240	Λεωφ. Μεσογείων 94, Αθήνα 115 27	Athens	Πολύ ωραία βόλτα, και πολλά παιχνίδια για τους τετράποδους φίλους μας	\N
2	Πάρκο Χαμοστέρνας	0103000020E6100000010000000B000000646916DB2DB537403623A8AC4AFB42404A8327BA36B537408481A7BD45FB4240DFD88CDF41B537403A0BBA8F45FB4240FE3AD9F84AB537404A33C37845FB42403CFF712B5DB53740B4A9B0A645FB4240FF637CF376B537409AE8F35146FB4240A74A91B178B537407EBE9EC34AFB42408D52C33969B5374018B3BA7E4AFB4240C9DF55624EB537407A4EB1954AFB4240DC17B1FE38B537404263F35F4AFB4240646916DB2DB537403623A8AC4AFB4240	Π. Τσαλδάρη 111, Καλλιθέα 176 72	Athens	Λίγο παραμελημένο αλλά με αρκετά δέντρα και χωμάτινο σκάμμα.	\N
\.


--
-- TOC entry 5726 (class 0 OID 17640)
-- Dependencies: 228
-- Data for Name: dogwalks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dogwalks (id, title, geometry, location, city, comment, image) FROM stdin;
1	Δάσος Κέρης	0102000020E61000004E000000B01C210379043940CEA96400A8AA4140AC4901B38C043940FAE648788CAA41402A60F18A96043940C786C9AF7AAA4140CBB7E3F2C40439401114E40C6AAA4140985EACB9ED0439406C4E6F905AAA41403C212A430B0539407110638852AA414057F036CA55053940F8E4BC5A49AA4140D13307527305394075D256804AAA414064AA059BDF053940EDFDFCAD53AA414087EB072B0406394069EB96D354AA4140D67BE01923063940F1BFF0A54BAA414046B1DCD26A06394045D5AF743EAA41407C1BAC49010739404CFA7B293CAA414014A639C31E083940BB9D7DE541AA4140D49F580284083940F8E4BC5A49AA4140F6AC10FBA90839407CF7223548AA4140B3D30FEA2209394079944A7842AA41407638BA4A77093940C6843D9237AA41406D5E3013A00939408F62CAD12DAA4140688B10C3B3093940A26E563321AA414060E5D022DB0939409F0B7E761BAA41405D46FB69ED093940642717BE19AA41402D584F52050A3940E37789A020AA414048F31142510A3940E014B1E31AAA41409EF5DF394A0A394092C5A28E33AA4140CADC216A470A39406529A3DB5CAA414048F31142510A3940821ABE8575AA414099BA2BBB600A3940EF5EA40689AA414077AD73C23A0A3940E7DABC1699AA41408087FDF9110A394034CBAF308EAA4140B448C961E6093940EF5EA40689AA41409879BCDA9B0939407DF9AE528BAA4140F821CA726D09394073710AE187AA41402471A0D167093940CAE9A16C80AA4140FC28345A580939403C4F97207EAA41402CE395DA4109394040B26FDD83AA4140D9B3E73235093940B57A3D4E87AA41400AD6DDE11B09394047D73B9281AA41408F5EC3C2FF083940B93C31467FAA4140FBB37AE294083940FEA83C7084AA4140B15E56725F0839406C4C3E2C8AAA41400C00FA22460839406FAF16E98FAA41403CEEA53A2E0839403009BC3896AA4140ED9117E30D083940FAE648788CAA4140CA501553E9073940B57A3D4E87AA4140D45EE921BF073940D5D0611976AA41402E008DD2A50739401477BCC96FAA41405DBAEE528F0739405DA5BBEB6CAA41406A6798DA52073940CF0AB19F6AAA4140A702EE79FE0639409FAEEE586CAA4140DA5B25B3D5063940D26D895C70AA4140B34703D3C4063940916456EF70AA4140665309AAA1063940D26D895C70AA414094D920938C063940C423F1F274AA4140EFAE0EDB71063940FB4564B37EAA414071981E03680639403BF07BE58BAA4140C89AECFA60063940AA937DA191AA41402843FA9232063940E477E45993AA41408318E8DA17063940E7DABC1699AA414088539C59010639406BED22F197AA414060D7E54AF3053940F2C17CC38EAA4140BBACD392D8053940388DA32886AA4140C4865DCAAF053940026B30687CAA4140A279A5D189053940CEAB956478AA414000EE68D25C053940447463D57BAA41405F622CD32F05394088E06EFF80AA4140BE0A3A6B01053940B57A3D4E87AA41403C5574DA090539407733FED87FAA414034AF343A31053940CB48BDA772AA4140D8A5FC5A4D053940988922A46EAA4140CD60E701870539409FAEEE586CAA4140728BF9B9A10539409C4B169C66AA41403ECA2D52CD053940DE54490966AA4140B7D9B342EC053940DE54490966AA41402C4A647A1D063940D72F7D5468AA41407F7912222A0639409C4B169C66AA41407F45C88A2B0639405E04D7265FAA41402D7EAE111C063940A732D6485CAA4140	Τύλισος 715 00	Heraklion	Έυκολη διαδρομή με όμορφη θέα και πολύ χώρο να παίξουν οι τετράποδοι φίλοι μας	\N
3	Φιλοπάππου	0102000020E610000017000000D85EB0C0FCB6374065F8F47DDDFB4240A9D898D711B73740E3056C62DCFB424062F316B435B7374036F0598DDBFB42405DECACCC4AB73740E3056C62DCFB4240DB029DA454B737407CAA549ADEFB42404529215855B7374008C3256CE4FB42401A42DF2758B737401B0FB6D8EDFB4240024B091C64B7374046B18119F8FB4240258C0BAC88B737400513245B02FC4240F59D5F94A0B73740912BF52C08FC4240F096F5ACB5B737405572A9A514FC424030D63730B9B73740FD21ECCA1DFC4240C1DC932CCCB73740C08D39741FFC424027FCADF8E1B7374096C6D40220FC4240CC26C0B0FCB737403550CF7124FC42408948A8740BB8374027C4B70B28FC4240C5B4CAA722B837406D7EB2182BFC424018DF6124C5B73740321F10E84CFC4240F1CA3F44B4B73740D029C8CF46FC424048CD0D3CADB73740FE56FCF03DFC424050734DDC85B7374056CC52FC29FC4240DB029DA454B73740CE3EEA0A11FC424062F316B435B73740EE3B2B0E0CFC4240	Φυλής 215, Αθήνα 117 41	Athens	Πολύ ωραία βόλτα στο κέντρο της Αθήνας, με πράσινο και μνημεία και πολλά σκυλάκια να μαζεύονται τριγύρω	\N
4	ΗΣΑΠ Ταύρος - Θησείο	0102000020E610000014000000ADA987C32DB437405EB818A831FB4240BEF49B2E30B437400D8D278238FB42401579ED2D40B43740EB6F09C03FFB424088CB3B985EB43740D37833B44BFB4240EBC9FCA36FB437400BA7165B52FB42402FE065868DB437409A362DC25EFB424052D735B5C7B437404025F8F076FB4240D38D0B62FBB4374046EEE9EA8EFB42405447D80121B537409A8EA5B4A3FB424087D569EE32B537407A6CCB80B3FB4240DEDB3EF559B5374072A9A514CFFB4240843A9B4473B53740784485EAE6FB4240F4A3E194B9B53740686B8EBD28FC4240548D5E0D50B637400C9BB7A0ADFC42403558DD8F80B6374046A28625D4FC4240FC8FA740C1B637409248916BF9FC424016719582C9B63740FF9DA34401FD4240A2F20A9F08B73740CFE8FD350FFD4240709DDA745FB737405068FE3D1DFD4240CDE26A099EB737402ECFDE7426FD4240	Π. Τσαλδάρη 141, Καλλιθέα 176 76	Athens	Βόλτα χωρίς πολλά αυτοκίνητα να σε διακόπτουν γιατί υπάρχει ποδηλατόδρομος και μεγαλα παρτέρια για παιχνίδι στο Θησείο	\N
5	Δάσος Φουρνί	0102000020E61000001A00000063A6A3D23E2A3940CB1F1D684FA041406DB477A1142A3940FC7BDFAE4DA041404CDE0033DF2939403E85121C4DA04140FEB5BC72BD29394059BA27B451A04140B1C1C2499A293940295E656D53A04140BD06D8A260293940CB1F1D684FA041409AC5D5123C2939408A16EAFA4FA04140A8A6C931FE283940A779C7293AA041408565C7A1D9283940FEC00B1126A04140074FD7C9CF283940C86D45AC0FA04140DAFF006BD5283940AE4F94DFFD9F41405E51A5C1C82839401BBE8575E39F4140061B8D32D1283940F97A08F4D39F4140AB459FEAEB283940EFF26382D09F41407C8B3D6A0229394030FC96EFCF9F4140A8A6C931FE28394097AB1F9BE49F414073B1B3322B2939400F08196DFA9F4140EDF483BA48293940D89DEE3CF19F41403B51121269293940828472ECEA9F4140B1C1C2499A293940A7412CF6F29F4140792DD791D9293940F9C907F30DA041406F1F03C3032A3940E4A25A4414A04140BAA871CA372A39400949B08229A04140E1F0DD41472A3940A779C7293AA04140D44334BA832A3940FD92437A40A04140F8B880E1A62A3940D6BE25A545A04140	Π. Τσαλδάρη 141, Καλλιθέα 176 76	Heraklion	Όμορφο πευκοδάσος για βόλτα, προσοχή μπορεί να συναντήσετε κάποιο αδέσποτο σκυλάκι	\N
12	Πεδίον Άρεως	0102000020E61000000C00000046A6D943A4BB37404475AD9E25FF4240E50ECB64CCBB374008C17CDE1CFF4240733D560A3BBC3740045021BD17FF42404CA6262554BC37403CA6D47014FF4240F0BD9CB481BC37403CA6D47014FF42409F0D354D94BC3740C66D26E011FF4240ACC1EC9DAABC3740F00C91D618FF42407EC8909AFEBC37406E6E61E926FF4240FD863A8A1FBD37400433DD6B20FF424082DBF6B938BD37400433DD6B20FF42407BFADA5944BD3740DE067DDB23FF4240F18976B886BD37403EBE28D20DFF4240	Λεωφ. Αλεξάνδρας, Αθήνα 106 82	Athens	Ωραία βόλτα στο κέντρο της πόλης γεμάτη πράσινο.	\N
7	Πάρκο Ιλισίων	0102000020E61000000C000000B9F4A8CE79C237403C12E558A7FC4240C9D92A7755C23740720404CEADFC4240CBAC4AC741C23740BCA31012B3FC424040790E1B1BC23740344BB846BAFC4240302878AFFFC13740B83D4162BBFC4240CEDB7D33D6C1374048BCE1E3B8FC42403DA1D79FC4C13740F6D1F3B8B9FC4240067069EB96C1374028BFA0E0BDFC4240A18499B67FC137402EE5E896C2FC4240A92AD95658C13740EAD04433AAFC42406A1FE16A53C137406E299DFEA2FC424096D2D80352C137403E3CF0D69EFC4240	Ορμινιου 34, Αθήνα 115 28	Athens	Μικρή και όμορφη βόλτα.	\N
6	Υμηττός	0102000020E610000024000000A7C2E96EE8CD3740B289271653FB4240CED60B4FF9CD37404B2E104E55FB42400DE2033BFECD37406CAA93D85AFB4240CED60B4FF9CD3740E6513B0D62FB4240CF0A56E6F7CD3740C5B01E5267FB4240CA03ECFE0CCE3740643A19C16BFB424073011E0714CE3740D8FCAEBE70FB42408E97C9CBF5CD37405689682A7AFB42406DBE5B6ACECD3740C7E52E7887FB4240F619619B9ECD3740797187F2AAFB4240273C574A85CD3740CD36DCECB4FB4240AB4F83B3A5CC37409F09A8CBBDFB424000AE64C746CC3740D75C24A3B9FB4240D9CD8C7E34CC37408C987E2EBFFB4240DAC87553CACB374083723678BAFB4240217AADDFA7CB3740F3F395F6BCFB4240529CA38E8ECB374039AE9003C0FB42406A93799A82CB374055450257C3FB42406D324F5370CB37409F09A8CBBDFB4240E1325D3E48CB3740797187F2AAFB424092A2844F29CB3740123B095BA2FB424027B04A3327CB37403C832B4597FB4240737511F0B5CB374065F0E65F81FB424042542B5D0BCC3740FE8B56A478FB424013D21A834ECC3740A128756E7FFB424061FA5E4370CC3740DE978E9488FB4240DA09E5338FCC3740B06A5A7391FB42401E215E32E9CC3740B44F6CAA93FB42400C6D4AC33ACD37407C2189038DFB4240DCB2E84251CD374044F3A55C86FB424033816CA34BCD37407220DA7D7DFB42401547D4FA11CD37403AF2F6D676FB42404401367BFBCC3740CA95308969FB42404401367BFBCC37403EA2F8E758FB4240701CC242F7CC37405E9F39EB53FB4240D397EF2AB5CC37400674154152FB4240	Unnamed Road, Καισαριανή	Athens	τα σκυλάκια ξετρελένονται με τόσο οξυγόνο και φύση	\N
11	Πάρκο Σταύρος Νιάρχος	0102000020E61000000C000000ED3E168EDFB03740204D825872F842401288BBA0DCB037401C2E47CF7AF84240FE17A7D8D3B0374000D29C9480F842404072E799C9B03740E2DA74F785F8424053B3A42FC6B03740C0AD51958AF842406552102ADBB0374014D84D3D93F8424098A31837EDB03740F82A739F8EF8424052FB599E1AB137405A59943F83F84240D0F4EB4FA9B1374042D4E588B3F842402F91F084D3B137409C77661FA4F84240359F7C10F8B13740DE3D345596F84240D5D0D7BD0FB23740DE3D345596F84240	Λεωφ. Ανδρέα Συγγρού 364, Καλλιθέα 176 74	Athens	ωραία βόλτα με πολλά ερεθίσματα για τα σκυλάκια.	\N
\.


--
-- TOC entry 5722 (class 0 OID 17622)
-- Dependencies: 224
-- Data for Name: petspointofinterest; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.petspointofinterest (id, name, category, geometry, address, city, comment, image) FROM stdin;
5	Pets & Friends	pet shop	0101000020E6100000A31FCC4992D83740D461B2217E054340	Αναπαύσεως 47, Βριλήσσια 152 35	Athens	Ποιοτικό pet shop!!	\N
8	Κτηνιατρείο Ελένη Χαλασοχώρη	vet	0101000020E6100000637B642FDDB63740A2815B86BAF74240	Αγνώστων Μαρτύρων 76, Νέα Σμύρνη 171 23	Athens	Εξαιρετική Δουλειά	\N
1	VetCheck	vet	0101000020E6100000B02A2240CCB4374098DCDC4C2DFB4240	Κρέμου 9, Καλλιθέα 176 76	Athens	Εξαιρετικός κτηνίατρος 10/10!	\N
40	10/09 Δέκα Ενάτου	coffee shop	0101000020E6100000BB3C7EE886B437404A7366A732FB4240	Χαροκόπου 143, Καλλιθέα 176 76	Athens	Pet friendly caffe!! Υπέροχο μέρος, ευγενικό προσωπικό	\N
4	Pets & Friends	pet shop	0101000020E61000000D6A885EA7B637402890010C69F84240	Λεωφ. Ελ. Βενιζέλου 109, Νέα Σμύρνη 171 23	Athens	\N	\N
38	zoo kennel	pet hotel	0101000020E61000002AE16405E8E337405CFD62095BF74240	ΘΕΣΗ ΠΟΥΣΙ ΛΕΔΙ, Παιανία 190 02	Athens	Απλό και οικονομικό ξενοδοχείο σκύλων. Με εξειδικευμένο προσωπικό.	\N
6	Peggy Sue	coffee shop	0101000020E6100000ACFA400E11B737408A7DF7561BFA4240	Σπαθαρη 2, Νέα Σμύρνη 171 21	Athens	Τίμιο & Pet friendlyFF	\N
34	Κτηνιατρικό Κέντρο Πειραιά	pet hospital	0101000020E6100000C3FFD25242A737404A44D794F7F84240	Γρ. Λαμπράκη 54-56, 185 32, Πειραιάς	Athens	Αξιόπιστη κλινική	\N
35	Aroanides	Mountain hotel	0101000020E610000070251091A22A3640BC58B95943F84240	Πλανητέρο 250 07	Επαρχία Καλαβρύτων	Pet friendly ξενοδοχείο, δίπλα σε πλατανόδασος!!	\N
3	Pawse Καλλιθέα	pet shop	0101000020E6100000E0185D39D6B237405962AFC10CFA4240	Λεωφ. Ελ. Βενιζέλου 193, Καλλιθέα 176 73	Athens	Μεγάλη ποικιλία σε παιχνίδια και τροφές!!	\N
\.


--
-- TOC entry 5558 (class 0 OID 16707)
-- Dependencies: 219
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- TOC entry 5737 (class 0 OID 0)
-- Dependencies: 225
-- Name: dogparks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dogparks_id_seq', 15, true);


--
-- TOC entry 5738 (class 0 OID 0)
-- Dependencies: 227
-- Name: dogwalks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dogwalks_id_seq', 17, true);


--
-- TOC entry 5739 (class 0 OID 0)
-- Dependencies: 223
-- Name: petspointofinterest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.petspointofinterest_id_seq', 65, true);


--
-- TOC entry 5568 (class 2606 OID 17638)
-- Name: dogparks dogparks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dogparks
    ADD CONSTRAINT dogparks_pkey PRIMARY KEY (id);


--
-- TOC entry 5570 (class 2606 OID 17647)
-- Name: dogwalks dogwalks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dogwalks
    ADD CONSTRAINT dogwalks_pkey PRIMARY KEY (id);


--
-- TOC entry 5566 (class 2606 OID 17629)
-- Name: petspointofinterest petspointofinterest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.petspointofinterest
    ADD CONSTRAINT petspointofinterest_pkey PRIMARY KEY (id);


-- Completed on 2025-03-02 17:28:36

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-03-02 17:28:36

--
-- PostgreSQL database cluster dump complete
--


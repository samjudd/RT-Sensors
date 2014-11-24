/** @jsx React.DOM */
var Play = React.createClass({
    render: function(){
        return (<i className="fa fa-play-circle fa-4x" onclick="connect();"></i>
               );
    }
});
var Stop = React.createClass({
    render: function(){
        return (<i className="fa fa-pause fa-3x" onclick="terminate();"></i>
               );
    }
});
var SensorController = React.createClass({
    getInitialState: function(){
        return {playing: true};
    },
    flip: function(){
        this.setState({
            playing : !(this.state.playing)
        });
    },
    render: function(){
        var controlButton;
        if(this.state.playing){
            controlButton = <Play />;
        }else{
            controlButton = <Stop />;
        }
        return (
            <div className="col-md-2">
                <a className="btn btn-lg no-padding icon" href="#" onClick={this.flip}>
                {controlButton}
                </a>
            </div>
        );
    }
});

var SensorMiniGraph = React.createClass({
    render: function(){
        return (
            <div className="col-md-10 minigraph" id={'minigraph'+this.props.id}>
            Empty filler
            </div>
        );
    }
});
        
var SensorInfoBody = React.createClass({
    render: function(){
        return (
            <div className="panel-body no-padding">
                    <div className ="row">
                        <SensorController />
                        <SensorMiniGraph id={this.props.id}/>
                    </div>
            </div>
        )
    }
});

var SensorInfoHead = React.createClass({
    render: function(){
        return (
            <div className="panel-heading">
                <ul className="list-inline no-margin">
                    <li>AIN#</li>&nbsp;
                    <li><input type="text" className="form-control" placeholder="Sensor name" /></li>
                    <li className="pull-right">mu = 20V sigma = +- 3V</li>
                </ul>
            </div>
               );
    }
});

var SensorInfo = React.createClass({
    render: function() {
        return (
            <div className="panel panel-primary">
                <SensorInfoHead />
                <SensorInfoBody id={this.props.id}/>
            </div>
        );
    }
});

var Sensors = React.createClass({
    render: function() {
        var sensors = [];
        for (i=0;i<=2;i++){
            sensors.push(<SensorInfo key={'sensor'+i} id={(i).toString()}/>);
        };                         
        return (
            <div className="col-md-5">
                {sensors}
            </div>
        );
    }
});
    
var Graph = React.createClass({
    render: function() {
        return (
            <div className="col-md-6">
                <div id="maingraph" className="biggraph"></div>
            </div>
        );
    }
});
    
var App = React.createClass({
    render: function(){
        return (
            <div className="row">
                <Sensors />
                <Graph />
            </div>
        );
    }
});

React.render(<App />, document.getElementById('container'));

$('#maingraph').highcharts(example1);
$('#minigraph0').highcharts(example2);